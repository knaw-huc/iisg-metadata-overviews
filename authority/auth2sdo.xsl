<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:marc="http://www.loc.gov/MARC21/slim"
    xmlns:sdo="https://schema.org/"
    exclude-result-prefixes="xsl">

<xsl:output method="xml" encoding="UTF-8" indent="yes"/>
<xsl:strip-space elements="*"/>

<xsl:template match="marc:record">
    <rdf:RDF>
        <rdf:Description>
            <xsl:attribute name="rdf:about">
                <xsl:text>https://iisg.amsterdam/authority/</xsl:text>
                <xsl:call-template name="set-URItype"/>
                <xsl:value-of select="marc:controlfield[@tag='001']"/>
            </xsl:attribute>
            <xsl:apply-templates select="marc:datafield"/>
        </rdf:Description>
    </rdf:RDF>
</xsl:template>

<xsl:template match="marc:leader"/>
<xsl:template match="marc:controlfield"/>

<xsl:template match="marc:datafield[@tag='035']">
    <xsl:call-template name="set-authorityURI">
        <xsl:with-param name="authfilenumber" select="normalize-space(substring-after(marc:subfield[@code='a'], ')'))"/>
        <xsl:with-param name="source" select="substring-after(substring-before(marc:subfield[@code='a'], ')'), '(')"/>
    </xsl:call-template>
</xsl:template>

<xsl:template match="marc:datafield[@tag='040']"/>

<xsl:template match="marc:datafield[@tag='100']">
    <!-- 100 - Heading - Personal Name -->
    <rdf:type rdf:resource='https://schema.org/Person'/>
    <sdo:name>
        <xsl:value-of select="marc:subfield[@code='a']"/>
    </sdo:name>
</xsl:template>

<xsl:template match="marc:datafield[@tag='110']">
    <!-- 110 - Heading - Corporate Name -->
    <rdf:type rdf:resource='https://schema.org/Organization'/>
    <sdo:name>
        <xsl:value-of select="marc:subfield[@code='a']"/>
    </sdo:name>
</xsl:template>

<xsl:template match="marc:datafield[@tag='111']">
    <!-- 111 - Heading - Meeting Name -->
    <rdf:type rdf:resource='https://schema.org/Event'/>
    <sdo:name>
        <xsl:value-of select="marc:subfield[@code='a']"/>
        <xsl:text> </xsl:text>
        <xsl:value-of select="marc:subfield[@code='d']"/>
        <xsl:text> </xsl:text>
        <xsl:value-of select="marc:subfield[@code='c']"/>
    </sdo:name>
</xsl:template>

<xsl:template match="marc:datafield[@tag='130']">
    <!-- 130 - Heading - Uniform Title -->
</xsl:template>

<xsl:template match="marc:datafield[@tag='148']">
    <!-- 148 - Heading - Chronological Term -->
    <rdf:type rdf:resource='https://schema.org/DefinedTerm'/>
    <sdo:name>
        <xsl:value-of select="marc:subfield[@code='a']"/>
    </sdo:name>
</xsl:template>

<xsl:template match="marc:datafield[@tag='150']">
    <!-- 150 - Heading - Topical Term -->
    <rdf:type rdf:resource='https://schema.org/DefinedTerm'/>
    <sdo:name>
        <xsl:value-of select="marc:subfield[@code='a']"/>
    </sdo:name>
</xsl:template>

<xsl:template match="marc:datafield[@tag='151']">
    <!-- 151 - Heading - Geographic Name -->
    <rdf:type rdf:resource='https://schema.org/Place'/>
    <sdo:name>
        <xsl:value-of select="marc:subfield[@code='a']"/>
    </sdo:name>
</xsl:template>

<xsl:template match="marc:datafield[@tag='155']">
    <!-- 155 - Heading - Genre/Form Term -->
    <rdf:type rdf:resource='https://schema.org/DefinedTerm'/>
    <sdo:name>
        <xsl:value-of select="marc:subfield[@code='a']"/>
    </sdo:name>
</xsl:template>

<xsl:template match="marc:datafield[@tag='400']">
    <sdo:alternateName>
        <xsl:value-of select="marc:subfield[@code='a']"/>
    </sdo:alternateName>
</xsl:template>

<xsl:template match="marc:datafield[@tag='450']">
    <sdo:alternateName>
        <xsl:value-of select="marc:subfield[@code='a']"/>
    </sdo:alternateName>
</xsl:template>

<xsl:template match="marc:datafield[@tag='550']">
    <sdo:alternateName>
        <xsl:value-of select="marc:subfield[@code='a']"/>
    </sdo:alternateName>
</xsl:template>

<xsl:template match="marc:datafield[@tag='901']"/>

<!-- named templates -->

<xsl:template name="set-authorityURI">
    <xsl:param name="source"/>
    <xsl:param name="authfilenumber"/>
    <xsl:choose>
        <xsl:when test="$source = 'VIAF'">
            <sdo:sameAs>
                <xsl:attribute name="rdf:resource">
                    <xsl:text>http://viaf.org/viaf/</xsl:text>
                    <xsl:value-of select="normalize-space(translate($authfilenumber, ' ()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', '                                                       '))"/>
                </xsl:attribute>
            </sdo:sameAs>
        </xsl:when>
        <xsl:when test="$source = 'DLC'">
            <sdo:sameAs>
                <xsl:attribute name="rdf:resource">
                    <xsl:text>http://id.loc.gov/authorities/subjects/sh</xsl:text>
                    <xsl:value-of select="normalize-space(translate($authfilenumber, ' ()', '                                                       '))"/>
                </xsl:attribute>
            </sdo:sameAs>
        </xsl:when>
    </xsl:choose>
</xsl:template>

<xsl:template name="set-URItype">
    <xsl:choose>
        <xsl:when test="marc:datafield[@tag='100']">
            <xsl:text>person/</xsl:text>
        </xsl:when>
        <xsl:when test="marc:datafield[@tag='110']">
            <xsl:text>organization/</xsl:text>
        </xsl:when>
        <xsl:when test="marc:datafield[@tag='111']">
            <xsl:text>event/</xsl:text>
        </xsl:when>
        <xsl:otherwise>
            <xsl:text>NotDeterminedYet/</xsl:text>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>


</xsl:stylesheet>
