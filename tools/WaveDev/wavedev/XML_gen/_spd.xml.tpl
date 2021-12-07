<?xml version="1.0" encoding="UTF-8"?>
<softpkg id="DCE:Default" name="DefaultResource">
	<title />
    <description></description>
	<author>
		<name>OSSIE Project</name>
		<company>Mobile and Portable Radio Research Group</company>
		<webpage>http://www.mprg.org</webpage>
	</author>
	<propertyfile type="PRF">
		<localfile name="Default.prf.xml"></localfile>
	</propertyfile>
	<descriptor>
		<localfile name="Default.scd.xml"/>
	</descriptor>
	<implementation id="DCE:Default">
		<description>Description</description>
		<code type="Executable">
			<localfile name="./default/default"/>
		</code>
		<processor name="x86"/>
	</implementation>
</softpkg>
