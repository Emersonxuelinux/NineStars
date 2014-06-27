#!/usr/bin/python
#coding:utf8
import subprocess
import time
import os
import shutil
try:
    from configobj import ConfigObj
except ImportError:
    print "please install configobj modules like 'easy_install configobj'."


class dbUpdate(object):
    """about dragonball jar package update and database file update."""

    @staticmethod
    def Update_Jar(UJargs):
        """dragonball jar package update.
        1.modify for needs update files.
        2.running about shell commands to update the jar packages.
        3.Usage:
            classname.dbUpdate.Update_Jar(D)
            the D like this:
                D={'ConfigFile':'one.txt','sysCF':'sysConfig.properties','dbCF':'dbConfig.properties','sId':i,'DBIp':DBIp}
        """
        #1
        with open(UJargs['WDir']+UJargs['ConfigFile'],'r') as f:
            PortConfigS=f.readlines()

        PortConfig=PortConfigS[int(UJargs['sId'])-1].split(',')
        sysConf = ConfigObj(UJargs['WDir'] + UJargs['CF'] + 'sysConfig.properties')
        sysConf['socketGame.ip'] = "0.0.0.0"
        sysConf['socketGame.port'] = PortConfig[1]
        sysConf['socketGm.port'] = PortConfig[2]
        sysConf['socketRecharge.port'] = PortConfig[3]
        sysConf['net.environment'] = PortConfig[0]
        sysConf.write()

        dataConf = ConfigObj(UJargs['WDir'] + UJargs['CF'] + 'dataConfig.properties')
        if UJargs['A_I'] == 'android':
            dataConf['recharge.type'] = "1"
        elif UJargs['A_I'] == 'ios':
            dataConf['recharge.type'] = "2"
        dataConf.write()

        dbConf = ConfigObj(UJargs['WDir'] + UJargs['CF'] + 'dbConfig.properties')
        dbConf['url'] = "jdbc:mysql://{0}/{1}".format(PortConfig[4],PortConfig[5])
        dbConf['user'] = PortConfig[6]
        dbConf['password'] = PortConfig[7].strip()
        dbConf.write()
        
        #jar command package(JarCmd_p) , file of copy(JarCmd_f), notice of update info(JarCmd_n). notice and sql file  move to /tmp dir for temp backup.(JarCmd_nm)
        JarCmd_p="jar uvf r-server.jar {0}*.properties".format(UJargs['UDIR'])
        JarCmd_f="cp r-server.jar {0}{1}/{1}.jar".format(UJargs['TDIR'],UJargs['STag']+str(UJargs['sId']))
        
        SPsql = 'db{0}.sql'.format(str(UJargs['sId']))
        if SPsql in os.listdir('{0}{1}'.format(UJargs['WDir'],UJargs['A_I'])):
            JarCmd_n="cp {2}/updateInfo.txt {2}/{3} {0}{1}".format(UJargs['TDIR'],UJargs['STag']+str(UJargs['sId']),UJargs['A_I'],SPsql)
        else:
            JarCmd_n="cp {2}/updateInfo.txt {2}/*.sql {0}{1}".format(UJargs['TDIR'],UJargs['STag']+str(UJargs['sId']),UJargs['A_I'])
            
        if os.path.exists(UJargs['TDIR']+UJargs['STag']+str(UJargs['sId'])) is False:
            os.makedirs(UJargs['TDIR']+UJargs['STag']+str(UJargs['sId']))
            print "create dir successful"

        subprocess.Popen("dos2unix {0}*".format(UJargs['CF']),shell=True,cwd=UJargs['WDir']).communicate()
        subprocess.Popen(JarCmd_p, shell=True,cwd=UJargs['WDir']).communicate()
        
        if os.path.exists("{0}/updateInfo.txt".format(UJargs['TDIR']+UJargs['STag']+str(UJargs['sId']))):
            NowTmpDir = "/tmp/{0}/{1}/".format(time.strftime("%Y-%m-%d-%H-%M", time.localtime()), UJargs['STag']+str(UJargs['sId']))
            JarCmd_nm="mv {0}/updateInfo.txt {0}/*.sql {0}/db*.jar {1}".format(UJargs['TDIR']+UJargs['STag']+str(UJargs['sId']), NowTmpDir)
            subprocess.Popen('mkdir -p {0}'.format(NowTmpDir), shell=True).communicate()
            subprocess.Popen(JarCmd_nm, shell=True,cwd=UJargs['WDir']).communicate()
        subprocess.Popen(JarCmd_n, shell=True,cwd=UJargs['WDir']).communicate()
        subprocess.Popen(JarCmd_f, shell=True,cwd=UJargs['WDir']).communicate()

        
def Exec_Update():
    CF="com/huayi/djgame2/dragonball/common/config/system/"
    #make output dir
    TargetDir='/data/DB/DBAndroid/'
    #make output sub dir
    SerTag='db'
    #make a distinction between android and ios platform.
    MPlat='android'
    #make package source dir
    WorkDir="/data/shell/servertest/"
    #update about new jar and rename.
    subprocess.Popen('svn up', shell=True, cwd=WorkDir).communicate()
    subprocess.Popen('cp serverB.jar r-server.jar', shell=True, cwd=WorkDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
    #print ConfigList
    for i in [1,2,3,4]:
        print "{0}-{1}-{2}".format(MPlat, SerTag, i)      
        ConfigList={'ConfigFile':'PortConfigure.conf','CF':CF,'sId':i,'TDIR':TargetDir,'UDIR':CF,'STag':SerTag,'A_I':MPlat,'WDir':WorkDir}
        
        dbUpdate.Update_Jar(ConfigList)

Exec_Update()            
            