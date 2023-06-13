import xml.etree.ElementTree as ET

import requests
from fastapi import FastAPI, Response

JSON_URL = "https://launchercontent.mojang.com/javaPatchNotes.json"

app = FastAPI()


@app.get("/feed.rss")
async def root():
    response = requests.get(JSON_URL)

    response.raise_for_status()

    data = response.json()

    if data["version"] != 1:
        raise Exception("Data version mismatch!")

    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")

    title = ET.SubElement(channel, "title")
    title.text = "Minecraft updates"

    link = ET.SubElement(channel, "link")
    link.text = JSON_URL

    description = ET.SubElement(channel, "description")
    description.text = "Minecraft update patch notes as displayed in the launcher"

    image = ET.SubElement(channel, "image")
    image_url = ET.SubElement(image, "url")
    image_url.text = (
        "https://www.minecraft.net/etc.clientlibs/minecraft/clientlibs/main/resources"
        "/favicon-96x96.png"
    )

    image_title = ET.SubElement(image, "title")
    image_title.text = "Minecraft"

    image_link = ET.SubElement(image, "link")
    image_link.text = JSON_URL

    for entry in data["entries"]:
        item = ET.SubElement(channel, "item")

        title = ET.SubElement(item, "title")
        title.text = entry["title"]

        description = ET.SubElement(item, "description")
        description.text = (
            f'<img src="https://launchercontent.mojang.com/{entry["image"]["url"]}" '
            f'alt="{entry["image"]["title"]}" '
            'style="float: right">'
        ) + entry["body"]

        guid = ET.SubElement(item, "guid")
        guid.text = entry["id"]

    ET.indent(rss)

    return Response(
        ET.tostring(rss, method="xml", encoding="utf8"), media_type="application/xml"
    )
