# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta as delta
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class komponen(models.Model):
    _name = 'komponen'
    _description = 'Komponen'

    name = fields.Char(string='Nama Komponen', required=True, )
    waktu_pengerjaan = fields.Integer()


class komponen_item(models.Model):
    _name = 'komponen.item'
    _description = 'Item komponen'

    name = fields.Char(string='Nama Item', required=True, )
    line_ids = fields.One2many(
        'komponen.item.detail',
        'item_id',
        string='Komponen',
    )
    tanggal_mulai = fields.Date('Mulai Pengerjaan', )
    tanggal_expektasi = fields.Date(
        'Expektasi', compute='get_date_expexted')
    tanggal_selesai = fields.Date('Tanggal Selesai', )

    @api.one
    @api.depends('tanggal_mulai')
    def get_date_expexted(self):
        if self.tanggal_mulai and self.line_ids:
            wp = max(sum([line.komponen_id.waktu_pengerjaan for line in self.line_ids if line.komponen_id]) - 1, 0)
            print 'wp', wp
            te = fields.Date.from_string(self.tanggal_mulai) + delta(days=wp)
            self.tanggal_expektasi = te
        else:
            self.tanggal_expektasi = False

    @api.one
    @api.constrains('line_ids')
    def _check_bobot(self):
        msg = "Jumlah persentase seluruh komponen tidak boleh melebihi 100%"
        bobot = sum([line.bobot for line in self.line_ids])
        print bobot, 'bobot'
        if bobot > 100:
            raise ValidationError(msg)


class komponen_item_detail(models.Model):
    _name = 'komponen.item.detail'
    _description = 'Komponen detail'

    item_id = fields.Many2one('komponen.item', 'Komponen', )
    komponen_id = fields.Many2one('komponen', 'Komponen', )
    bobot = fields.Float(string='Bobot Presentase', digits=(3, 1))
