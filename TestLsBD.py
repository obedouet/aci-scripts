from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.access import DnQuery
from cobra.model.fv import Tenant, Ctx, BD, RsCtx, Ap, AEPg, RsBd, RsDomAtt

apicUrl = 'https://172.16.31.36'
loginSession = LoginSession(apicUrl, 'admin', 'Tel1dus!')
moDir = MoDirectory(loginSession)
moDir.login()

dnQuery = DnQuery('uni/tn-LAN01')
dnQuery.subtree = 'children'
tenantMo = moDir.query(dnQuery)
for obj in tenantMo:
    print obj.dn
    for _BD in obj.BD:
	print _BD.dn
    for _app in obj.AP:
	print _app.dn
moDir.logout()
