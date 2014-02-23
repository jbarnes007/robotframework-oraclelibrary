'''
Copyright 03/01/2014 Jules Barnes

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import cx_Oracle as DB
from robot.libraries.BuiltIn import BuiltIn

class keywords(object):

    def __init__(self):
        """
        """
        self._connection = None
        self._default_log_level = 'INFO'
        self._bexception = False
        self.robotBuiltIn = BuiltIn()

    def _ora_connect(self, dbName):
        """
        """   
        connectionSettings = self.robotBuiltIn.get_variable_value("${" + dbName + "}")
    
        if connectionSettings == None:
            self.robotBuiltIn.log((("No database connection configured for %s") % (dbName)), "WARN")
            return 99
        else:
            if connectionSettings["dbConnectionType"].upper() == "SID":
                dbTns = DB.makedsn(connectionSettings["dbServerName"], 
                                   connectionSettings["dbServerPort"],
                                   connectionSettings["dbServerId"])
                
            elif connectionSettings["dbConnectionType"].upper() == "SERVICE":
                dbTns = (("%s:%s/%s") % (connectionSettings["dbServerName"], 
                                         connectionSettings["dbServerPort"],
                                         connectionSettings["dbServerId"]))                
            else:
                self.robotBuiltIn.fail((("Unknown connection type configured for %s. Only SID & SERVICE types are supported.") % (dbName)))
                
            connString = (("%s/%s@%s") % (connectionSettings["dbUsername"], 
                                          connectionSettings["dbPassword"], 
                                          dbTns))
            
            return self.ora_make_connection(connString)
        
        
    def ora_make_connection(self, sConnString):
        """
        """
        sConn = None
        try:
            sConn = DB.connect(sConnString )
        except Exception:
            self._bexception = True
            print 'Connection for database has failed', Exception, sConnString
            raise 
        finally:
            self._connection = sConn
        
        return sConn

    def ora_execute_sql (self, sSql=None, sServerId=None):
        """
        """
        if sServerId <> None:
            self._ora_connect(sServerId)
            
        sOut = None
        sCursor = None
        sConn = self._connection
        print sConn
        
        if (sConn == None) :
            return sOut
        else:
            try:
                sCursor = sConn.cursor()
                sCursor.execute(sSql)
                sOut = sCursor.fetchall()                   
                return sOut
            
            except Exception, err:
                raise Exception (('Query execution failed. %s') % (err))
            finally:
                if (sCursor <> None):
                    sCursor.close ()
                    
        self.ora_disconnect_from_database(sConn)

    def ora_disconnect_from_database (self,sConn=None):
        """
        """
        if (sConn <> None):
            sConn.close ()
        else:
            self._connection.close ()
        