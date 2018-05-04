import requests
import sys
import time
import json


def parseLines(file):
    with open(file) as f:
        content = f.readlines()

    content = [x.strip() for x in content]

    i = 0
    tsIndex = 0
    locIndex = 0

    params = []
    items = []

    locations = []

    for l in content:
        if i == 0:
            headers = l.split(",")
            hindex = 0
            for h in headers:
                if h == 'timestamp':
                    tsIndex = hindex
                else:
                    if h == 'location':
                        locIndex = hindex
                    else:
                        params.append({'name': h.replace(" ", ""), 'index': hindex})

                hindex = hindex + 1

            print("TS Idx " + str(tsIndex))
            print("LOC Idx " + str(locIndex))
            print("Found the following parameters: ")
            print(params)
        else:
            splitted = l.split(",")
            sindex = 0

            if len(splitted) == 1:
                continue

            joined = []

            realLoc = ""
            tojoin = 0

            for s in splitted:

                if tojoin == 1:
                    realLoc = realLoc + s
                    tojoin = 0
                    joined.append(realLoc)
                    continue

                if sindex == locIndex:
                    realLoc = s + ","
                    tojoin = 1
                else:
                    joined.append(s)

                # print("")
                # print(joined)
                sindex = sindex + 1

            sindex = 0
            for s in joined:
                item = {}
                item['location'] = joined[locIndex]

                if item['location'] not in locations:
                    locations.append(item['location'])

                item['timestamp'] = joined[tsIndex]

                if sindex == locIndex:
                    print()
                    # item['location'] = s
                else:
                    if sindex == tsIndex:
                        print()
                        # item['timestamp'] = s
                    else:
                        item['value'] = s

                        for p in params:
                            if p['index'] == sindex:
                                item['param'] = p['name']

                        # print(item)

                        items.append(item)

                sindex = sindex + 1

        i = i + 1

    return {'items': items, 'locations': locations}


def getFoi(o, existing):
    maxstnum = 1

    for featureOfInterest in existing['featureOfInterest']:

        if isinstance(featureOfInterest, str):
            continue

        numstr = int(featureOfInterest['name']['value'].split(" ")[1])

        if numstr > maxstnum:
            maxstnum = numstr

        lat = featureOfInterest['geometry']['coordinates'][0]
        lon = featureOfInterest['geometry']['coordinates'][1]

        mylat = o['location'].replace("\"", "").replace(" ", "").split(",")[0]
        mylon = o['location'].replace("\"", "").replace(" ", "").split(",")[1]

        if str(lat) == str(mylat):

            if str(lon) == str(mylon):
                foi = "<gml:identifier codeSpace=\"\">" + featureOfInterest['identifier']['value'] + "</gml:identifier>\n"
                foi += "<gml:name>" + featureOfInterest['name']['value'] + "</gml:name>\n"

                return {'fois': existing, 'thisfoi': foi}

    idnum = str(int(round(time.time() * 1000)))
    statsnum = str(maxstnum + 1)
    mylat = o['location'].replace("\"", "").replace(" ", "").split(",")[0]
    mylon = o['location'].replace("\"", "").replace(" ", "").split(",")[1]

    newfoi = {
        "identifier": {
            "codespace": "http://www.opengis.net/def/nil/OGC/0/unknown",
            "value": "http://arduino.geodab.eu/gpw/featureOfInterest/" + idnum
        },
        "name": {
            "codespace": "http://www.opengis.net/def/nil/OGC/0/unknown",
            "value": "ESA " + statsnum
        },
        "sampledFeature": "http://arduino.geodab.eu/gpw/featureOfInterest/1",
        "geometry": {
            "type": "Point",
            "coordinates": [
                float(mylat),  # 41.827374,
                float(mylon)  # 12.674041
            ]
        }
    }

    print("Created new foi")
    print(newfoi)

    existing['featureOfInterest'].append(newfoi)

    foi = "                            <gml:identifier codeSpace=\"\">http://arduino.geodab.eu/gpw/featureOfInterest/" + idnum + "</gml:identifier>\n"
    foi += "                            <gml:name>ESA " + statsnum + "</gml:name>\n"

    return {'fois': existing, 'thisfoi': foi}


def insertObservation(ob, millis, procedure, fois, oprefix):
    newfois = getFoi(ob, fois)

    # print(newfois)

    enriched = newfois['fois']
    foi = newfois['thisfoi']

    jj = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    jj += "<env:Envelope\n"
    jj += "    xmlns:env=\"http://www.w3.org/2003/05/soap-envelope\"\n"
    jj += "    xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.w3.org/2003/05/soap-envelope http://www.w3.org/2003/05/soap-envelope/soap-envelope.xsd\">\n"
    jj += "    <env:Body>\n"
    jj += "        <sos:InsertObservation\n"
    jj += "            xmlns:sos=\"http://www.opengis.net/sos/2.0\"\n"
    jj += "            xmlns:swes=\"http://www.opengis.net/swes/2.0\"\n"
    jj += "            xmlns:swe=\"http://www.opengis.net/swe/2.0\"\n"
    jj += "            xmlns:sml=\"http://www.opengis.net/sensorML/1.0.1\"\n"
    jj += "            xmlns:gml=\"http://www.opengis.net/gml/3.2\"\n"
    jj += "            xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n"
    jj += "            xmlns:om=\"http://www.opengis.net/om/2.0\"\n"
    jj += "            xmlns:sams=\"http://www.opengis.net/samplingSpatial/2.0\"\n"
    jj += "            xmlns:sf=\"http://www.opengis.net/sampling/2.0\" service=\"SOS\" version=\"2.0.0\" xsi:schemaLocation=\"http://www.opengis.net/sos/2.0 http://schemas.opengis.net/sos/2.0/sos.xsd            http://www.opengis.net/samplingSpatial/2.0 http://schemas.opengis.net/samplingSpatial/2.0/spatialSamplingFeature.xsd\">\n"
    jj += "            <!-- multiple offerings are possible -->\n"
    # jj += "            <sos:offering>http://www.52north.org/test/offering/9</sos:offering>\n"
    jj += "            <sos:offering>http://arduino.geodab.eu/gpw/offering/" + oprefix + "TR_OBSERVABLE</sos:offering>\n"
    jj += "            <sos:observation>\n"
    jj += "                <om:OM_Observation gml:id=\"o1\">\n"
    jj += "                    <gml:description>test description for this observation</gml:description>\n"
    jj += "                    <gml:identifier codeSpace=\"\">http://arduino.geodab.eu/gpw/observation/TR_OBSNUMBER</gml:identifier>\n"
    jj += "                    <om:type xlink:href=\"http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement\"/>\n"
    jj += "                    <om:phenomenonTime>\n"
    jj += "                        <gml:TimeInstant gml:id=\"phenomenonTime\">\n"
    jj += "                            <gml:timePosition>TR_TIMEPOSITION</gml:timePosition>\n"
    # jj += "                            <gml:timePosition>2012-11-19T17:45:15.000+00:00</gml:timePosition>\n"
    jj += "                        </gml:TimeInstant>\n"
    jj += "                    </om:phenomenonTime>\n"
    jj += "                    <om:resultTime xlink:href=\"#phenomenonTime\"/>\n"
    jj += "                    <om:procedure xlink:href=\"" + procedure + "\"/>\n"
    # jj += "                    <om:observedProperty xlink:href=\"http://www.52north.org/test/observableProperty/9_3\"/>\n"
    jj += "                    <om:observedProperty xlink:href=\"http://arduino.geodab.eu/gpw/observableProperty/TR_OBSERVABLE\"/>\n"
    jj += "                    <om:featureOfInterest>\n"
    jj += "                        <sams:SF_SpatialSamplingFeature gml:id=\"ssf_test_feature_9\">\n"
    # jj += "                            <gml:identifier codeSpace=\"\">http://www.52north.org/test/featureOfInterest/9</gml:identifier>\n"
    # jj += "                            <gml:name>ESA 1</gml:name>\n"
    jj += foi
    jj += "                            <sf:type xlink:href=\"http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingPoint\"/>\n"
    jj += "                            <sf:sampledFeature xlink:href=\"http://arduino.geodab.eu/gpw/featureOfInterest/1\"/>\n"
    jj += "                            <sams:shape>\n"
    jj += "                                <gml:Point gml:id=\"test_feature_9\">\n"
    # jj += "                                    <gml:pos srsName=\"http://www.opengis.net/def/crs/EPSG/0/4326\">51.935101100104916 7.651968812254194</gml:pos>\n"
    jj += "                                    <gml:pos srsName=\"http://www.opengis.net/def/crs/EPSG/0/4326\">TR_COORDINATES</gml:pos>\n"
    jj += "                                </gml:Point>\n"
    jj += "                            </sams:shape>\n"
    jj += "                        </sams:SF_SpatialSamplingFeature>\n"
    jj += "                    </om:featureOfInterest>\n"
    # jj += "                    <om:result xsi:type=\"gml:MeasureType\" uom=\"test_unit_9_3\">0.28</om:result>\n"
    jj += "                    <om:result xsi:type=\"gml:MeasureType\" uom=\"test_unit_9_3\">TR_RESULT</om:result>\n"
    jj += "                </om:OM_Observation>\n"
    jj += "            </sos:observation>\n"
    jj += "        </sos:InsertObservation>\n"
    jj += "    </env:Body>\n"
    jj += "</env:Envelope>"

    jj = jj.replace("TR_OBSNUMBER", str(millis))
    jj = jj.replace("TR_RESULT", ob['value'].replace("\"", ""))
    jj = jj.replace("TR_OBSERVABLE", ob['param'].replace("\"", ""))

    # ol = ob['location'].replace("\"", "")
    #
    # reverse = []
    # sp = ol.split(",")
    #
    # reverse.append(sp[1])
    # reverse.append(sp[0])
    # jj = jj.replace("TR_COORDINATES", reverse[0] + " " + reverse[1])

    locationtowritetmp = ob['location'].replace("\"", "")

    locationtowrite = locationtowritetmp.split(",")[0].replace(" ", "")

    locationtowrite = locationtowrite + " " + locationtowritetmp.split(",")[1].replace(" ", "")

    jj = jj.replace("TR_COORDINATES", locationtowrite)

    jj = jj.replace("TR_TIMEPOSITION", ob['timestamp'].replace(" ", "T").replace("\"", ""))

    headers = {'Content-Type': 'application/soap+xml'}

    print("Executing POST for " + ob['param'] + " ...")
    #print("loc: " + ob['location'])
    #print("loc to write: " + locationtowrite)
    #print(jj)

    r = requests.post("http://arduino.geodab.eu/52n-sos-webapp/service", data=jj, headers=headers)

    print("Request completed with code: " + str(r.status_code))

    return enriched


ar = sys.argv[2].split("/")

offprefix = ar[len(ar) - 1]

parsed = parseLines(sys.argv[1])

parsedItems = parsed['items']
print(parsed['locations'])
print("Parsed " + str(len(parsedItems)) + " items")

millis = int(round(time.time() * 1000))

itemidx = 0

headers = {'Content-Type': 'application/json'}

print("Executing Get FOI...")
gfoir = "{\"request\": \"GetFeatureOfInterest\",\"service\": \"SOS\",\"version\": \"2.0.0\",\"procedure\": \"" + sys.argv[
    2] + "\"}"

print(gfoir)
r = requests.post("http://arduino.geodab.eu/52n-sos-webapp/service",
                  data=gfoir,
                  headers=headers)

fois = json.loads(r.content.decode('utf-8'))

e = fois
for item in parsedItems:
    e = insertObservation(item, millis=millis + itemidx, procedure=sys.argv[2], fois=e, oprefix=offprefix)
    itemidx = itemidx + 1
