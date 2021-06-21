import math
import time
from typing import Optional
import xml.etree.ElementTree as ET
from http.client import RemoteDisconnected

import requests
from fastapi import APIRouter, HTTPException, Path

from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/metrics")
async def instance_get_metrics(
    cluster_id: str = Path(default=None, title="cluster_id", description="Cluster ID"),
    vm_uuid: str = Path(default=None, title="vm_uuid", description="VM UUID"),
    start: Optional[int] = None,
    interval: Optional[int] = 60,
):
    """Get Xen Host Metrics"""

    xen_clusters = Settings.get_xen_clusters()

    try:
        cluster_data = xen_clusters[cluster_id]

        session = requests.Session()
        session.auth = (cluster_data["username"], cluster_data["password"])

        url = cluster_data["host"] + "/rrd_updates"

        if start is None:
            start = math.floor(time.time() - interval)

        response = session.get(
            url,
            params=dict(
                start=start,
                interval=interval,
                cf="AVERAGE",
            ),
        )

        xml = ET.ElementTree(ET.fromstring(response.text))
        xml_root = xml.getroot()
        x_metadata = xml_root.find("meta")
        x_legend = x_metadata.find("legend")

        entries = x_legend.findall("entry")

        x_data = xml_root.find("data")
        x_rows = x_data.findall("row")

        data = dict()

        for i, legend_tag in enumerate(entries):
            name = legend_tag.text
            is_relavant = "vm:" + vm_uuid in name

            if is_relavant:
                # data_type = name.split(":")[0]
                data_name = name.split(":")[3]

                data[data_name] = []

                for row in x_rows:
                    timestamp = int(row.find("t").text)
                    value = float(row.findall("v")[i].text)

                    data[data_name].append(
                        dict(
                            timestamp=timestamp,
                            value=value,
                        )
                    )

        return dict(
            success=True,
            data=data,
        )

    except NameError:
        raise HTTPException(
            status_code=404,
            detail="Specified cluster_id does not exist",
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)
