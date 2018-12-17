<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" >

<xsl:template match="/">
<html><head><title>--xml + xsl via python lxml--</title></head>
<body>
<h3>sample.xml + sample.xsl > html</h3>
<table style="border-collapse:collapse">
<tr>
<td style="background:#93d5dc; border:1px solid #333; border-collapse:collapse; padding:8">Name</td>
<td style="background:#93dca5; border:1px solid #333; border-collapse:collapse; padding:8">Access</td>
<td style="background:#e3d8a5; border:1px solid #333; border-collapse:collapse; padding:8">Spot</td></tr>
<xsl:apply-templates/>
</table>
</body>
</html>
</xsl:template>

<xsl:template match="items">
<xsl:for-each select="item">
<tr>
<td style="background:#e0f0f0; border:1px solid #333; border-collapse:collapse; padding:8"><xsl:value-of select="name"/></td>
<td style="background:#e0f0e6; border:1px solid #333; border-collapse:collapse; padding:8"><xsl:value-of select="access/email"/></td>
<td style="background:#f0ede0; border:1px solid #333; border-collapse:collapse; padding:8"><xsl:value-of select="access/location"/></td>
</tr>
</xsl:for-each>
</xsl:template>

</xsl:stylesheet>