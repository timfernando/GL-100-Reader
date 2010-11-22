
KML_HEADER = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Mobile Oxford - Sociology Project</name>
    <description>Output from GL-100</description>
    <Style id="yellowLineGreenPoly">
      <LineStyle>
        <color>7f00ffff</color>
        <width>10</width>
      </LineStyle>
      <PolyStyle>
        <color>7f00ff00</color>
      </PolyStyle>
    </Style>
    <Placemark>
      <name>Our Path</name>
      <description>Path of the GL100</description>
      <styleUrl>#yellowLineGreenPoly</styleUrl>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>

        <coordinates>
    """
        
KML_FOOTER =  """
       </coordinates>
              </LineString>
            </Placemark>
          </Document>
        </kml>
        """
        
with open('default.output', 'r') as f_in:
        with open('default.kml', 'w') as f_out:
            f_out.write(KML_HEADER)
            for line in f_in:
                data = line.split(",")
                if data[0] == '+RESP:GTTRI':
                    responses = int(data[2]) # Check how many responses the GPS says it has sent
                    data = data[10:] # Get rid of header // useless initial data
                    for i in range(responses):
                        latitude = data[(i*15)]
                        longitude = data[(i*15)+1]
                        # Special case to make sure we're not registering 0,0 -- although this is not ideal
                        if float(longitude) != 0 and float(latitude) != 0:
                            f_out.write(latitude + "," + longitude + ",0" +"\n")
            f_out.write(KML_FOOTER)