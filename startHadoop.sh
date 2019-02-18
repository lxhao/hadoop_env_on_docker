#/bin/bash
 docker network create -o "com.docker.network.bridge.name"="hadoop" --subnet 100.10.0.0/16 hadoop
# hadoop的三个容器名字
hadoop_arr=("master" "slave1" "slave2");
# hadoop三个容器对应的ip地址
hadoop_ip=("100.10.0.100" "100.10.0.101" "100.10.0.102");
for((m=0;m<${#hadoop_arr[*]};m++));
do
    if [ ${hadoop_arr[$m]} = "master" ]
    then
        echo "master"
        docker run -tid --name ${hadoop_arr[$m]} -h ${hadoop_arr[m]} --add-host hadoop0:100.10.0.100 --add-host hadoop1:100.10.0.101 --add-host hadoop2:100.10.0.102 --net=hadoop --ip=${hadoop_ip[m]} -p 8088:8088 -p 50070:50070 hadoop:2.9
    else
        docker run -tid --name ${hadoop_arr[$m]} -h ${hadoop_arr[m]} --add-host hadoop0:100.10.0.100 --add-host hadoop1:100.10.0.101 --add-host hadoop2:100.10.0.102 --net=hadoop --ip=${hadoop_ip[m]} hadoop:2.9
    fi
done;

# format hdfs
docker exec ${hadoop_arr[0]} /usr/local/hadoop/bin/hdfs namenode -format
# 启动hadoop集群
docker exec ${hadoop_arr[0]} /root/startHadoop.exp
