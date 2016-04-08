# -*- coding: utf-8 -*-
##############################################################################
#
#    auth_login_as module for OpenERP, Allows the administrator to login as any other user, without the need to know his password
#    Copyright (C) 2016 SYLEAM Info Services (<http://www.Syleam.fr/>)
#              Sylvain Garancher <sylvain.garancher@syleam.fr>
#
#    This file is a part of auth_login_as
#
#    auth_login_as is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    auth_login_as is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api
from openerp import SUPERUSER_ID
from openerp.http import request


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def login_as(self):
        """
        Allows the administrator to login as this user, without knowing his password
        """
        self.ensure_one()
        if self.env.uid == SUPERUSER_ID:
            request.session.uid = self.id
            request.session.login = self.login
            request.session.password = -1
            request.session.login_from_admin = True
            request.uid = self.id

    @api.v7
    def check_credentials(self, cr, uid, password):
        """
        Return True if the user is logged from admin, call super instead
        """
        if request.session.get('login_from_admin'):
            return True

        return super(ResUsers, self).check_credentials(cr, uid, password)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
