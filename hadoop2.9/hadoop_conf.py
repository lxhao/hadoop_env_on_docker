import os
import sys, socket

def writeHadoopConfigFile(name,xml):
    f = open("/usr/local/hadoop/etc/hadoop/" + name,"w")
    f.write(xml)
    f.close()

mf = open("master","r")
sf = open("slaves","r")
mip = mf.read().strip()
sip = sf.read().replace("-","")
mf.close()
sf.close()

#core-site.xml
coreSiteXml = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <!-- Default HDFS ip and port -->
    <property>
         <name>fs.defaultFS</name>
         <value>hdfs://%(mip)s:9000</value>
    </property>
    <!-- default RPC IP,and use 0.0.0.0 to represent all ips-->
    <property>
	<name>dfs.namenode.rpc-bind-host</name>
	<value>0.0.0.0</value>
    </property>
</configuration>""" % dict(mip=mip)
writeHadoopConfigFile("core-site.xml",coreSiteXml)
hdfsSiteXml = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
       <name>dfs.permissions</name>
      <value>false</value>
   </property>
    <property>
        <name>dfs.namenode.http-address</name>
        <value>0.0.0.0:50070</value>
    </property>
    <property>
        <name>dfs.namenode.secondary.http-address</name>
        <value>0.0.0.0:50090</value>
    </property>
    <property>
        <name>dfs.replication</name>
        <value>2</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/data/hadoop/name</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/data/hadoop/data</value>
    </property>
</configuration>
"""
writeHadoopConfigFile("hdfs-site.xml",hdfsSiteXml)

mapredSiteXml = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
"""
writeHadoopConfigFile("mapred-site.xml",mapredSiteXml)

yarnSiteXml = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>%(mip)s</value>
    </property>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
         <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
         <value>org.apache.hadoop.mapred.ShuffleHandler</value>
    </property>
  <property>
    <name>yarn.resourcemanager.address</name>
    <value>%(mip)s:8032</value>
  </property>
  <property>
     <name>yarn.resourcemanager.scheduler.address</name>
     <value>%(mip)s:8030</value>
  </property>
  <property>
     <name>yarn.resourcemanager.resource-tracker.address</name>
     <value>%(mip)s:8031</value>
  </property>
  <property>
     <name>yarn.resourcemanager.admin.address</name>
     <value>0.0.0.0:8033</value>
   </property>
   <property>
      <name>yarn.resourcemanager.webapp.address</name>
      <value>0.0.0.0:8088</value>
   </property>
</configuration>
""" % dict(mip=mip)
writeHadoopConfigFile("yarn-site.xml",yarnSiteXml)
master = mip
writeHadoopConfigFile("master",master)
slaves = sip
writeHadoopConfigFile("slaves",slaves)
