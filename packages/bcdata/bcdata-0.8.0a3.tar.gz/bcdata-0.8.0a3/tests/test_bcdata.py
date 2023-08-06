import os

import rasterio
import pytest
from rasterio.coords import BoundingBox

import bcdata
from bcdata.wfs import get_capabilities

from geopandas.geodataframe import GeoDataFrame

AIRPORTS_PACKAGE = "bc-airports"
AIRPORTS_TABLE = "WHSE_IMAGERY_AND_BASE_MAPS.GSR_AIRPORTS_SVW"
UTMZONES_KEY = "utm-zones-of-british-columbia"
BEC_KEY = "biogeoclimatic-ecosystem-classification-bec-map"
ASSESSMENTS_TABLE = "whse_fish.pscis_assessment_svw"
GLACIERS_TABLE = "whse_basemapping.fwa_glaciers_poly"
STREAMS_TABLE = "whse_basemapping.fwa_stream_networks_sp"


def test_validate_table_lowercase():
    table = bcdata.validate_name(AIRPORTS_TABLE.lower())
    assert table == AIRPORTS_TABLE


def test_cache_file(tmp_path):
    get_capabilities(refresh=True, cache_file=tmp_path / ".bcdata_test")
    assert os.path.exists(tmp_path / ".bcdata_test")


def test_get_table_name_urlparse():
    # bcdc api query result["object_name"] is not correct WFS layer name,
    # use WFS resource url
    table = bcdata.get_table_name("natural-resource-nr-district")
    assert table == "WHSE_ADMIN_BOUNDARIES.ADM_NR_DISTRICTS_SPG"


def test_get_count():
    table = bcdata.get_table_name(UTMZONES_KEY)
    assert bcdata.get_count(table) == 6


def test_get_count_filtered():
    assert bcdata.get_count(UTMZONES_KEY, query="UTM_ZONE=10") == 1


def test_get_data_asgdf():
    gdf = bcdata.get_data(UTMZONES_KEY, query="UTM_ZONE=10", as_gdf=True)
    assert type(gdf) == GeoDataFrame


def test_get_null_gdf():
    gdf = bcdata.get_data(UTMZONES_KEY, query="UTM_ZONE=9999", as_gdf=True)
    assert type(gdf) == GeoDataFrame


def test_get_data_small():
    data = bcdata.get_data(AIRPORTS_TABLE)
    assert data["type"] == "FeatureCollection"


def test_get_data_lowercase():
    data = bcdata.get_data(AIRPORTS_TABLE, lowercase=True)
    assert "airport_name" in data["features"][0]["properties"].keys()


def test_get_data_crs():
    data = bcdata.get_data(AIRPORTS_TABLE, crs="EPSG:3005")
    assert (
        data["crs"]
        == """{"type":"name","properties":{"name":"urn:ogc:def:crs:EPSG::3005"}}"""
    )


def test_get_types():
    data = bcdata.get_types(AIRPORTS_TABLE)
    assert data[0] == "POINT"


def test_get_mixed_types():
    data = bcdata.get_types(GLACIERS_TABLE, 100)
    assert len(data) == 2


def test_get_types_z():
    data = bcdata.get_types(STREAMS_TABLE)
    assert data[0] == "LINESTRINGZ"


def test_get_features():
    data = [f for f in bcdata.get_features(AIRPORTS_TABLE)]
    assert len(data) == 455


def test_get_data_paged():
    data = bcdata.get_data(AIRPORTS_TABLE, pagesize=250)
    assert len(data["features"]) == 455


def test_get_data_count():
    data = bcdata.get_data(AIRPORTS_TABLE, count=100)
    assert len(data["features"]) == 100


def test_get_data_paged_count():
    data = bcdata.get_data(AIRPORTS_TABLE, pagesize=250, count=300)
    assert len(data["features"]) == 300


def test_get_data_sortby():
    data = bcdata.get_data(AIRPORTS_TABLE, count=1, sortby="AIRPORT_NAME")
    assert data["features"][0]["properties"]["AIRPORT_NAME"] == "100 Mile House Airport"


def test_cql_filter():
    data = bcdata.get_data(
        AIRPORTS_TABLE,
        query="AIRPORT_NAME='Terrace (Northwest Regional) Airport'",
    )
    assert len(data["features"]) == 1
    assert (
        data["features"][0]["properties"]["AIRPORT_NAME"]
        == "Terrace (Northwest Regional) Airport"
    )


def test_bounds_filter():
    data = bcdata.get_data(AIRPORTS_TABLE, bounds=[1188000, 377051, 1207437, 390361])
    assert len(data["features"]) == 8


def test_cql_bounds_filter():
    data = bcdata.get_data(
        AIRPORTS_TABLE,
        query="AIRPORT_NAME='Victoria International Airport'",
        bounds=[1167680.0, 367958.0, 1205720.0, 432374.0],
        bounds_crs="EPSG:3005",
    )
    assert len(data["features"]) == 1
    assert (
        data["features"][0]["properties"]["AIRPORT_NAME"]
        == "Victoria International Airport"
    )


def test_dem(tmpdir):
    bounds = [1046891, 704778, 1055345, 709629]
    out_file = bcdata.get_dem(bounds, os.path.join(tmpdir, "test_dem.tif"))
    assert os.path.exists(out_file)
    with rasterio.open(out_file) as src:
        stats = [
            {
                "min": float(b.min()),
                "max": float(b.max()),
                "mean": float(b.mean()),
            }
            for b in src.read()
        ]
    assert stats[0]["max"] == 3982


def test_dem_align(tmpdir):
    bounds = [1046891, 704778, 1055345, 709629]
    out_file = bcdata.get_dem(
        bounds, os.path.join(tmpdir, "test_dem_align.tif"), align=True
    )
    assert os.path.exists(out_file)
    with rasterio.open(out_file) as src:
        bounds = src.bounds
    bbox = BoundingBox(1046787.5, 704687.5, 1055487.5, 709787.5)
    assert bounds == bbox


def test_dem_rasterio(tmpdir):
    bounds = [1046891, 704778, 1055345, 709629]
    src = bcdata.get_dem(bounds, as_rasterio=True)
    stats = [
        {"min": float(b.min()), "max": float(b.max()), "mean": float(b.mean())}
        for b in src.read()
    ]
    assert stats[0]["max"] == 3982


# interpolation takes a while to run, comment out for for faster tests
# def test_dem_resample(tmpdir):
#    bounds = [1046891, 704778, 1055345, 709629]
#    out_file = bcdata.get_dem(bounds, os.path.join(tmpdir, "test_dem.tif"), interpolation="bilinear", resolution=50)
#    assert os.path.exists(out_file)
#    with rasterio.open(out_file) as src:
#        stats = [{'min': float(b.min()),
#                  'max': float(b.max()),
#                  'mean': float(b.mean())
#                  } for b in src.read()]
#    assert stats[0]['max'] == 3956.0


def test_dem_invalid_resample1():
    with pytest.raises(ValueError):
        bounds = [1046891, 704778, 1055345, 709629]
        bcdata.get_dem(bounds, "test_dem.tif", interpolation="cubic", resolution=50)


def test_dem_invalid_resample2():
    with pytest.raises(ValueError):
        bounds = [1046891, 704778, 1055345, 709629]
        bcdata.get_dem(bounds, "test_dem.tif", interpolation="bilinear")
