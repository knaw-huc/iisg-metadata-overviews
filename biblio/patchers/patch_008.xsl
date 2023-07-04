<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:marc="http://www.loc.gov/MARC21/slim"
    exclude-result-prefixes="xsl marc">
  <xsl:output method="xml" indent="yes"/>
  
  <!-- Template to match MARC 21 records -->
  <xsl:template match="marc:record">
    <xsl:copy>
       <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <!-- Identity template to copy elements and attributes -->
  <xsl:template match="@* | node()">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="marc:controlfield[@tag='008']">
    <marc:controlfield tag="008">
        <xsl:value-of select="substring(.,1,7)"/>
        <xsl:value-of select="substring(../marc:datafield[@tag='260']/marc:subfield[@code='c'], 1, 4)"/>
        <xsl:value-of select="substring(.,12)"/>
    </marc:controlfield>
  </xsl:template>

</xsl:stylesheet>
