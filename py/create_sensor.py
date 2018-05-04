import requests
import sys

headers = {'Content-Type': 'application/soap+xml'}

print("Executing POST ...")

ar = sys.argv[1].split("/")

offprefix = ar[len(ar)-1]




ff = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
ff += "<env:Envelope\n"
ff += "    xmlns:env=\"http://www.w3.org/2003/05/soap-envelope\"\n"
ff += "    xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.w3.org/2003/05/soap-envelope http://www.w3.org/2003/05/soap-envelope/soap-envelope.xsd http://www.opengis.net/sos/2.0 http://schemas.opengis.net/sos/2.0/sosInsertSensor.xsd     http://www.opengis.net/swes/2.0 http://schemas.opengis.net/swes/2.0/swes.xsd\">\n"
ff += "    <env:Body>\n"
ff += "        <swes:InsertSensor\n"
ff += "            xmlns:swes=\"http://www.opengis.net/swes/2.0\"\n"
ff += "            xmlns:sos=\"http://www.opengis.net/sos/2.0\"\n"
ff += "            xmlns:swe=\"http://www.opengis.net/swe/2.0\"\n"
ff += "            xmlns:sml=\"http://www.opengis.net/sensorml/2.0\"\n"
ff += "            xmlns:gml=\"http://www.opengis.net/gml/3.2\"\n"
ff += "            xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n"
ff += "            xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n"
ff += "            xmlns:gco=\"http://www.isotc211.org/2005/gco\"\n"
ff += "            xmlns:gmd=\"http://www.isotc211.org/2005/gmd\" service=\"SOS\" version=\"2.0.0\">\n"
ff += "            <swes:procedureDescriptionFormat>http://www.opengis.net/sensorml/2.0</swes:procedureDescriptionFormat>\n"
ff += "            <swes:procedureDescription>\n"
ff += "                <sml:PhysicalSystem gml:id=\"sensor1\">\n"
ff += "                    <!--Unique identifier -->\n"
ff += "                    <gml:identifier codeSpace=\"uniqueID\">"+sys.argv[1]+"</gml:identifier>\n"
ff += "                    <sml:identification>\n"
ff += "                        <sml:IdentifierList>\n"
ff += "                            <sml:identifier>\n"
ff += "                                <sml:Term definition=\"urn:ogc:def:identifier:OGC:1.0:longName\">\n"
ff += "                                    <sml:label>longName</sml:label>\n"
ff += "                                    <sml:value>"+sys.argv[2]+"</sml:value>\n"
ff += "                                </sml:Term>\n"
ff += "                            </sml:identifier>\n"
ff += "                            <sml:identifier>\n"
ff += "                                <sml:Term definition=\"urn:ogc:def:identifier:OGC:1.0:shortName\">\n"
ff += "                                    <sml:label>shortName</sml:label>\n"
ff += "                                    <sml:value>"+sys.argv[2]+"</sml:value>\n"
ff += "                                </sml:Term>\n"
ff += "                            </sml:identifier>\n"
ff += "                        </sml:IdentifierList>\n"
ff += "                    </sml:identification>\n"
ff += "                    <sml:capabilities name=\"offerings\">\n"
ff += "                        <sml:CapabilityList>\n"
ff += "                            <!-- Special capabilities used to specify offerings. -->\n"
ff += "                            <!-- Parsed and removed during InsertSensor/UpdateSensorDescription, \n"
ff += "\t\t\t\t\t         added during DescribeSensor. -->\n"
ff += "                            <!-- Offering is generated if not specified. -->\n"

for param in sys.argv[3].split(","):
    if "http://arduino.geodab.eu/gpw/procedure" in param:
        continue

    pname = param.replace(" ", "")

    ff += "                            <sml:capability name=\"humidityoff\">\n"
    ff += "                                <swe:Text definition=\"urn:ogc:def:identifier:OGC:offeringID\">\n"
    ff += "                                    <swe:label>"+pname+" with sensor "+sys.argv[2]+"</swe:label>\n"
    ff += "                                    <swe:value>http://arduino.geodab.eu/gpw/offering/"+offprefix+pname+"</swe:value>\n"
    ff += "                                </swe:Text>\n"
    ff += "                            </sml:capability>\n"

ff += "                        </sml:CapabilityList>\n"
ff += "                    </sml:capabilities>\n"
ff += "                    <sml:capabilities name=\"metadata\">\n"
ff += "                        <sml:CapabilityList>\n"
ff += "                            <!-- status indicates, whether sensor is insitu (true) \n"
ff += "                            or remote (false) -->\n"
ff += "                            <sml:capability name=\"insitu\">\n"
ff += "                                <swe:Boolean definition=\"insitu\">\n"
ff += "                                    <swe:value>true</swe:value>\n"
ff += "                                </swe:Boolean>\n"
ff += "                            </sml:capability>\n"
ff += "                            <!-- status indicates, whether sensor is mobile (true) \n"
ff += "                            or fixed/stationary (false) -->\n"
ff += "                            <sml:capability name=\"mobile\">\n"
ff += "                                <swe:Boolean definition=\"mobile\">\n"
ff += "                                    <swe:value>false</swe:value>\n"
ff += "                                </swe:Boolean>\n"
ff += "                            </sml:capability>\n"
ff += "                        </sml:CapabilityList>\n"
ff += "                    </sml:capabilities>\n"
ff += "                    <sml:featuresOfInterest>\n"
ff += "                        <sml:FeatureList definition=\"http://www.opengis.net/def/featureOfInterest/identifier\">\n"
ff += "                            <swe:label>ESA 0</swe:label>\n"
ff += "                            <sml:feature xlink:href=\"http://arduino.geodab.eu/gpw/featureOfInterest/9\"/>\n"
ff += "                        </sml:FeatureList>\n"
ff += "                    </sml:featuresOfInterest>\n"
ff += "                    <sml:inputs>\n"
ff += "                        <sml:InputList>\n"


for param in sys.argv[3].split(","):
    if "http://arduino.geodab.eu/gpw/procedure" in param:
        continue

    pname = param.replace(" ", "")
    ff += "                            <sml:input name=\"test_observable_property_3\">\n"
    ff += "                                <sml:ObservableProperty definition=\"http://arduino.geodab.eu/gpw/observableProperty/"+pname+"\"/>\n"
    ff += "                            </sml:input>\n"



ff += "                        </sml:InputList>\n"
ff += "                    </sml:inputs>\n"
ff += "                    <sml:outputs>\n"
ff += "                        <sml:OutputList>\n"


for param in sys.argv[3].split(","):
    if "http://arduino.geodab.eu/gpw/procedure" in param:
        continue

    pname = param.replace(" ", "")
    ff += "                            <sml:output name=\"test_observable_property_1_1\">\n"
    ff += "                                <swe:Quantity definition=\"http://arduino.geodab.eu/gpw/observableProperty/"+pname+"\">\n"
    ff += "                                    <swe:uom code=\"NOT_DEFINED\"/>\n"
    ff += "                                </swe:Quantity>\n"
    ff += "                            </sml:output>\n"

ff += "                           \n"
ff += "                        </sml:OutputList>\n"
ff += "                    </sml:outputs>\n"
ff += "                </sml:PhysicalSystem>\n"
ff += "            </swes:procedureDescription>\n"
ff += "            <!-- multiple values possible -->\n"

for param in sys.argv[3].split(","):
    if "http://arduino.geodab.eu/gpw/procedure" in param:
        continue

    pname = param.replace(" ", "")
    ff += "            <swes:observableProperty>http://arduino.geodab.eu/gpw/observableProperty/"+pname+"</swes:observableProperty>\n"

ff += "            <swes:metadata>\n"
ff += "                <sos:SosInsertionMetadata>\n"
ff += "                    <sos:observationType>http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement</sos:observationType>\n"
ff += "                    <sos:observationType>http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CategoryObservation</sos:observationType>\n"
ff += "                    <sos:observationType>http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CountObservation</sos:observationType>\n"
ff += "                    <sos:observationType>http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_TextObservation</sos:observationType>\n"
ff += "                    <sos:observationType>http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_TruthObservation</sos:observationType>\n"
ff += "                    <sos:observationType>http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_GeometryObservation</sos:observationType>\n"
ff += "                    <sos:observationType>http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_ComplexObservation</sos:observationType>\n"
ff += "                    <sos:observationType>http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_SWEArrayObservation</sos:observationType>\n"
ff += "                    <sos:observationType>http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_ReferenceObservation</sos:observationType>\n"
ff += "                    <!-- multiple values possible -->\n"
ff += "                    <sos:featureOfInterestType>http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingPoint</sos:featureOfInterestType>\n"
ff += "                </sos:SosInsertionMetadata>\n"
ff += "            </swes:metadata>\n"
ff += "        </swes:InsertSensor>\n"
ff += "    </env:Body>\n"
ff += "</env:Envelope>\n";

print(ff)

r = requests.post("http://arduino.geodab.eu/52n-sos-webapp/service", data=ff, headers=headers)

print("Request completed with code: " + str(r.status_code))
