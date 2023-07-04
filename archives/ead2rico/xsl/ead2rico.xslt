<?xml version="1.0" encoding="UTF-8"?>

<!-- XSLT stylesheet converting City Archives Amsterdam examples -->
<!-- Endocoded Archival Description 2002 (EAD) into Records in Contexts Ontology (RiC-O) 0.2-->
<!-- Ivo Zandhuis (ivo@zandhuis.nl) 20210628 -->
<!-- IZ 20230623 Start generalizing -->

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:rico="https://www.ica.org/standards/RiC/ontology#"
    xmlns:ead="urn:isbn:1-931666-22-9" 
    exclude-result-prefixes="xsl ead">

<xsl:output method="xml" encoding="UTF-8" indent="yes"/>
<xsl:strip-space elements="*"/>

<xsl:param name="baseUri">https://hdl.handle.net/10622/</xsl:param>

<!-- RDF wrap -->
<xsl:template match="ead:ead">
    <rdf:RDF>
        <!--xsl:apply-templates select="ead:eadheader"/-->
        <xsl:apply-templates select="ead:archdesc"/>
    </rdf:RDF>
</xsl:template>

<!-- templates for eadheader -->
<!-- TODO -->

<!-- templates for archdesc-components, looping hierarchy -->
<xsl:template match="ead:archdesc">
    <rico:RecordSet>
        <xsl:attribute name="rdf:about">
            <xsl:value-of select="$baseUri"/>
            <xsl:value-of select="ead:did/ead:unitid"/>
        </xsl:attribute>
        <xsl:apply-templates select="ead:did"/>
        <xsl:apply-templates select="ead:scopecontent | ead:accessrestrict | ead:controlaccess | ead:odd"/>
        <xsl:call-template name="set-recordsettype">
            <xsl:with-param name="type" select="@level"/>
        </xsl:call-template>
    </rico:RecordSet>
    <xsl:apply-templates select="ead:dsc">
        <xsl:with-param name="archnr" select="ead:did/ead:unitid"/>
    </xsl:apply-templates>
</xsl:template>

<xsl:template match="ead:dsc">
    <xsl:param name="archnr"/>
    <xsl:apply-templates select="ead:c | ead:c01">
        <xsl:with-param name="archnr" select="$archnr"/>
        <xsl:with-param name="level" select="'first'"/>
    </xsl:apply-templates>
</xsl:template>

<xsl:template match="ead:c | ead:c01 | ead:c02 | ead:c03 | ead:c04 | ead:c05 | ead:c06 | ead:c07 | ead:c08 | ead:c09 | ead:c10 | ead:c11 | ead:c12">
    <xsl:param name="archnr"/>
    <xsl:param name="level"/>
    <xsl:variable name="id">
        <xsl:choose>
            <xsl:when test="$level = 'first'">
                <xsl:value-of select="concat(concat($archnr, '#'), position())"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="concat(concat($archnr, '-'), position())"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>
    <rico:RecordSet>
        <xsl:attribute name="rdf:about">
            <xsl:value-of select="$baseUri"/>
            <xsl:value-of select="$id"/>
        </xsl:attribute>
        <rico:isOrWasIncludedIn>
            <xsl:attribute name="rdf:resource">
                <xsl:value-of select="$baseUri"/>
                <xsl:value-of select="$archnr"/>
            </xsl:attribute>
        </rico:isOrWasIncludedIn>
        <xsl:call-template name="set-recordsettype">
            <xsl:with-param name="type" select="@level"/>
        </xsl:call-template>
        <xsl:apply-templates select="ead:did">
            <xsl:with-param name="type" select="@level"/>
        </xsl:apply-templates>
        <xsl:apply-templates select="ead:scopecontent | ead:accessrestrict | ead:controlaccess | ead:odd"/>
    </rico:RecordSet>
    <xsl:apply-templates select="ead:c | ead:c01 | ead:c02 | ead:c03 | ead:c04 | ead:c05 | ead:c06 | ead:c07 | ead:c08 | ead:c09 | ead:c10 | ead:c11 | ead:c12">
        <xsl:with-param name="archnr" select="$id"/>
    </xsl:apply-templates>
</xsl:template>

<!-- templates for did elements -->
<xsl:template match="ead:did">
    <xsl:param name="type"/>
    <xsl:apply-templates select="ead:unitid">
        <xsl:with-param name="type" select="$type"/>
    </xsl:apply-templates>
    <xsl:apply-templates select="ead:unittitle"/>
    <xsl:apply-templates select="ead:unitdate"/>
    <xsl:apply-templates select="ead:physdesc"/>
    <xsl:apply-templates select="ead:origination"/>
    <xsl:apply-templates select="ead:langmaterial"/>
    <xsl:apply-templates select="ead:repository"/>
</xsl:template>

<xsl:template match="ead:unitid">
    <xsl:param name="type"/>
    <rico:hasOrHadIdentifier>
        <rico:Identifier>
            <rico:textualValue>
                <xsl:value-of select="."/>
            </rico:textualValue>
            <xsl:call-template name="set-identifiertype">
                <xsl:with-param name="type" select="$type"/>
            </xsl:call-template>
        </rico:Identifier>
    </rico:hasOrHadIdentifier>
</xsl:template>

<xsl:template match="ead:unittitle">
    <rico:hasOrHadTitle>
        <rico:Title>
            <rico:textualValue>
                <xsl:value-of select="normalize-space(.)"/>
            </rico:textualValue>
        </rico:Title>
    </rico:hasOrHadTitle>
</xsl:template>

<xsl:template match="ead:unitdate">
    <rico:isAssociatedWithDate>
        <rico:DateRange>
            <rico:expressedDate>
                <xsl:value-of select="normalize-space(.)"/>
            </rico:expressedDate>
        </rico:DateRange>
    </rico:isAssociatedWithDate>
</xsl:template>

<xsl:template match="ead:physdesc">
    <rico:recordResourceExtent>
        <xsl:value-of select="normalize-space(.)"/>
    </rico:recordResourceExtent>
</xsl:template>

<xsl:template match="ead:origination">
    <rico:hasAccumulator>
        <xsl:apply-templates/>
    </rico:hasAccumulator>
</xsl:template>

<xsl:template match="ead:repository">
    <rico:hasOrHadHolder>
        <xsl:apply-templates/>
    </rico:hasOrHadHolder>
</xsl:template>

<xsl:template match="ead:langmaterial">
    <rico:hasOrHadSomeMembersWithLanguage>
        <rico:Language>
            <xsl:attribute name="rdf:about">
                <xsl:text>http://id.loc.gov/vocabulary/iso639-2/</xsl:text>
                <xsl:value-of select="ead:language/@langcode"/>
            </xsl:attribute>            
        </rico:Language>
    </rico:hasOrHadSomeMembersWithLanguage>
</xsl:template>

<!-- templates for non-did elements -->
<xsl:template match="ead:scopecontent">
    <rico:scopeAndContent>
        <xsl:apply-templates/>
    </rico:scopeAndContent>
</xsl:template>

<xsl:template match="ead:accessrestrict">
    <rico:conditionsOfAccess>
        <xsl:apply-templates/>
    </rico:conditionsOfAccess>
</xsl:template>

<xsl:template match="ead:controlaccess">
    <rico:hasOrHadSubject>
        <xsl:apply-templates/>
    </rico:hasOrHadSubject>
</xsl:template>

<xsl:template match="ead:odd">
    <rico:descriptiveNote>
        <xsl:apply-templates/>
    </rico:descriptiveNote>
</xsl:template>

<!-- templates for names of agents, places and subjects -->
<xsl:template match="ead:persname">
    <rico:Person>
        <xsl:if test="starts-with(@authfilenumber, 'http')">
            <xsl:attribute name="rdf:about">
                <xsl:value-of select="@authfilenumber"/>
            </xsl:attribute>
        </xsl:if>
        <rico:hasOrHadAgentName>
            <rico:AgentName>
                <rico:textualValue>
                    <xsl:value-of select="normalize-space(.)"/>
                </rico:textualValue>
            </rico:AgentName>
        </rico:hasOrHadAgentName>
    </rico:Person>
</xsl:template>

<xsl:template match="ead:corpname">
    <rico:CorporateBody>
        <xsl:if test="starts-with(@authfilenumber, 'http')">
            <xsl:attribute name="rdf:about">
                <xsl:value-of select="@authfilenumber"/>
            </xsl:attribute>
        </xsl:if>
        <rico:hasOrHadAgentName>
            <rico:AgentName>
                <rico:textualValue>
                    <xsl:value-of select="normalize-space(.)"/>
                </rico:textualValue>
            </rico:AgentName>
        </rico:hasOrHadAgentName>
    </rico:CorporateBody>
</xsl:template>

<xsl:template match="ead:famname">
    <rico:Family>
        <xsl:if test="starts-with(@authfilenumber, 'http')">
            <xsl:attribute name="rdf:about">
                <xsl:value-of select="@authfilenumber"/>
            </xsl:attribute>
        </xsl:if>
        <rico:hasOrHadAgentName>
            <rico:AgentName>
                <rico:textualValue>
                    <xsl:value-of select="normalize-space(.)"/>
                </rico:textualValue>
            </rico:AgentName>
        </rico:hasOrHadAgentName>
    </rico:Family>
</xsl:template>

<xsl:template match="ead:geogname">
    <rico:Place>
        <xsl:if test="starts-with(@authfilenumber, 'http')">
            <xsl:attribute name="rdf:about">
                <xsl:value-of select="@authfilenumber"/>
            </xsl:attribute>
        </xsl:if>
        <rico:hasOrHadPlaceName>
            <rico:PlaceName>
                <rico:textualValue>
                    <xsl:value-of select="normalize-space(.)"/>
                </rico:textualValue>
            </rico:PlaceName>
        </rico:hasOrHadPlaceName>
    </rico:Place>
</xsl:template>

<xsl:template match="ead:genreform | ead:subject">
    <rico:Thing>
        <xsl:if test="starts-with(@authfilenumber, 'http')">
            <xsl:attribute name="rdf:about">
                <xsl:value-of select="@authfilenumber"/>
            </xsl:attribute>
        </xsl:if>
        <rico:hasOrHadName>
            <rico:Name>
                <rico:textualValue>
                    <xsl:value-of select="normalize-space(.)"/>
                </rico:textualValue>
            </rico:Name>
        </rico:hasOrHadName>
    </rico:Thing>
</xsl:template>


<!-- text organizing templates-->
<xsl:template match="ead:p">
    <xsl:value-of select="normalize-space(.)"/>
    <xsl:text> </xsl:text>
</xsl:template>

<!-- empty templates-->
<xsl:template match="ead:address"/>
<xsl:template match="ead:head"/>

<!-- named templates -->
<xsl:template name="set-recordsettype">
    <xsl:param name="type"/>
    <xsl:choose>
        <xsl:when test="$type = 'fonds'">
            <rico:hasRecordSetType>
                <xsl:attribute name="rdf:resource">
                    <xsl:text>https://www.ica.org/standards/RiC/vocabularies/recordSetTypes#Fonds</xsl:text>
                </xsl:attribute>
            </rico:hasRecordSetType>
        </xsl:when>
        <xsl:when test="$type = 'collection'">
            <rico:hasRecordSetType>
                <xsl:attribute name="rdf:resource">
                    <xsl:text>https://www.ica.org/standards/RiC/vocabularies/recordSetTypes#Collection</xsl:text>
                </xsl:attribute>
            </rico:hasRecordSetType>
        </xsl:when>
        <xsl:when test="$type = 'series'">
            <rico:hasRecordSetType>
                <xsl:attribute name="rdf:resource">
                    <xsl:text>https://www.ica.org/standards/RiC/vocabularies/recordSetTypes#Series</xsl:text>
                </xsl:attribute>
            </rico:hasRecordSetType>
        </xsl:when>
        <xsl:when test="$type = 'subseries'">
            <rico:hasRecordSetType>
                <xsl:attribute name="rdf:resource">
                    <xsl:text>https://www.ica.org/standards/RiC/vocabularies/recordSetTypes#Subseries</xsl:text>
                </xsl:attribute>
            </rico:hasRecordSetType>
        </xsl:when>
        <xsl:when test="$type = 'file'">
            <rico:hasRecordSetType>
                <xsl:attribute name="rdf:resource">
                    <xsl:text>https://www.ica.org/standards/RiC/vocabularies/recordSetTypes#File</xsl:text>
                </xsl:attribute>
            </rico:hasRecordSetType>
        </xsl:when>
    </xsl:choose>
</xsl:template>

<xsl:template name="set-identifiertype">
    <xsl:param name="type"/>
    <xsl:choose>
        <xsl:when test="$type = 'fonds'">
            <rico:hasIdentifierType>
                <rico:IdentifierType>
                    <rico:name>Archiefnummer</rico:name>
                </rico:IdentifierType>
            </rico:hasIdentifierType>
        </xsl:when>
        <xsl:when test="$type = 'collection'">
            <rico:hasIdentifierType>
                <rico:IdentifierType>
                    <rico:name>Archiefnummer</rico:name>
                </rico:IdentifierType>
            </rico:hasIdentifierType>
        </xsl:when>
        <xsl:when test="$type = 'series'">
            <rico:hasIdentifierType>
                <rico:IdentifierType>
                    <rico:name>Rubriekscode</rico:name>
                </rico:IdentifierType>
            </rico:hasIdentifierType>
        </xsl:when>
        <xsl:when test="$type = 'subseries'">
            <rico:hasIdentifierType>
                <rico:IdentifierType>
                    <rico:name>Rubriekscode</rico:name>
                </rico:IdentifierType>
            </rico:hasIdentifierType>
        </xsl:when>
        <xsl:when test="$type = 'otherlevel'">
            <rico:hasIdentifierType>
                <rico:IdentifierType>
                    <rico:name>Inventarisnummers</rico:name>
                </rico:IdentifierType>
            </rico:hasIdentifierType>
        </xsl:when>
        <xsl:when test="$type = 'file'">
            <rico:hasIdentifierType>
                <rico:IdentifierType>
                    <rico:name>Inventarisnummer</rico:name>
                </rico:IdentifierType>
            </rico:hasIdentifierType>
        </xsl:when>
    </xsl:choose>
</xsl:template>

</xsl:stylesheet>
