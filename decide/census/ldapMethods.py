from ldap3 import Server, Connection, ALL_ATTRIBUTES
import re
class LdapCensus:
    #Este metodo establece una conexion con el servidor ldap pasado por parametros, el objecto direccion
    #es devuelto al final. urlServer es la dirección ldap junto con el puerto, auth debe ser el rdn del usuario
    #administrador del servidor, finalmente psw debe ser la contraseña de este.
    def ldapConnectionMethod(self, urlServer, auth, psw):
        server = Server(urlServer)
        conn = Connection(server, auth, psw, auto_bind=True)
        return conn

    #Este metodo llama al primero para establecer una conexion y posteriormente hacer una busqueda por la rama
    #indicada donde se encuentran los usuarios a añadir en el censo.
    def LdapGroups(self, LdapUrl, auth, psw, branch):
        conn = LdapCensus().ldapConnectionMethod(LdapUrl, auth, psw)
        conn.search(search_base=branch, search_filter='(objectclass=*)', attributes=[ALL_ATTRIBUTES])
        ldapList = []
        print(conn.entries)
        for entries in conn.entries:
            text = str(entries)
            group = re.findall('uid=(.+?),', text, re.DOTALL)
            for element in group:
                if group and ldapList.count(element) == 0:            
                    ldapList.append(element)
        return ldapList



