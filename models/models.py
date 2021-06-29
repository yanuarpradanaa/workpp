# -*- coding: utf-8 -*-

from odoo import models, fields, api
import math

class ProductionPP(models.Model):
	_inherit = 'mrp.production'

	no_spk = fields.Integer("No. Job")
	
	pelanggan = fields.Many2one('res.partner', string="Pelanggan",required=True)
	
	cetak_baru = fields.Boolean("Cetak Baru")
	repeat = fields.Boolean("Repeat")
	proof = fields.Boolean("Proof")

	repeat_perubahan = fields.Text("Repeat Perubahan")
	deadline = fields.Date("Deadline Akhir",required=True)

	acuan = fields.Text("Acuan")
	keterangan = fields.Text("Keterangan")

class BOMPP(models.Model):
	_inherit = 'mrp.bom'

	kategori = fields.Char(related="product_tmpl_id.categ_id.name",string="Category")

	kertas_prima = fields.Boolean("Prima")
	kertas_sendiri = fields.Boolean("Bawa Sendiri")

	jenis_kertas = fields.Many2one('product.template', 'Jenis Kertas',domain="[('default_code', 'like', 'PL-PA')]")
	# TODO : TAK GANTI PROPERTIES REQUIRED E
	ukuran_kertas = fields.Char("Ukuran Jadi")
	ukuran_potong = fields.Char("Ukuran Potong",required=True)

	# helper field
	# TODO : TAK GANTI MENJADI QUANTITY HELPER -> QUANTITY
	quantity = fields.Float(string="Quantity (pcs)",required=True,help="Tambahan data untuk perhitungan, harus sama dengan jumlah produk di manufacture order")

	lembar_plano = fields.Float("1 Lembar Plano jadi",required=True)
	lembar_druck = fields.Float("1 Lembar Druck jadi",required=True)

	insheet = fields.Float("Insheet",required=True)

	jumlah_druck = fields.Float("Jumlah Lembar Druck",readonly=False, compute='_compute_jumlah_druck',store=True)
	jumlah_plano = fields.Float("Jumlah Lembar Plano",readonly=False, compute='_compute_jumlah_plano',store=True)

	@api.depends('quantity','lembar_plano','lembar_druck','insheet')
	def _compute_jumlah_plano(self):
		for r in self:
			if (r.quantity and r.lembar_plano and r.lembar_druck and r.insheet) != 0:
				r.jumlah_plano = float(math.ceil(((r.quantity / r.lembar_druck) + r.insheet) / r.lembar_plano))

				self.product_qty = r.jumlah_plano

	@api.depends('jumlah_plano','lembar_plano')
	def _compute_jumlah_druck(self):
		for r in self:
			if r.jumlah_plano != 0:
				r.jumlah_druck = r.jumlah_plano * r.lembar_plano


				
class RoutingPP(models.Model):
	_inherit = 'mrp.routing.workcenter'

	## Cetak
	depan = fields.Boolean('Depan 4 Warna')
	# GANTI DEFAULT KOSONG
	depan_tambah_warna = fields.Text('Tambahan Warna Depan')
	belakang = fields.Boolean('Belakang 4 Warna')
	# GANTI DEFAULT KOSONG
	belakang_tambah_warna = fields.Text('Tambahan Warna Belakang')

	side1 = fields.Selection([('muka1', '1 Muka'), ('muka2', '2 Muka')],'Side 1',help="Isi 'Side 2' jika memilih '2 Muka'")
	side2 = fields.Selection([('balik', 'Balik Kertas'), ('anleg', 'Lain Anleg'),('plat','Lain Plat')],'Side 2')

	## Coating 
	coating_side = fields.Selection([('muka1', '1 Muka'), ('muka2', '2 Muka')],'Side')
	coating_ket = fields.Text('Keterangan')
	
	## Laminasi
	eflute_lain = fields.Text('Keterangan')

	## Finishing I
	# GANTI DEFAULT KOSONG
	spiral_lubang = fields.Char("Spiral Lubang",help="Isi field ini jika memilih 'Spiral'")
	spiral_ukuran = fields.Char("Ukuran Spiral",help="Isi field ini jika memilih 'Spiral'")
	spiral_warna = fields.Char("Warna Spiral",help="Isi field ini jika memilih 'Spiral'")

	## Lem
	pack_lem = fields.Selection([('samping', 'Lem Samping'),
		('bottom', 'Lock Bottom'),
		('manual','Lem Manual'),
		('sampingbottom','Lem Samping + Lock Bottom')],'Lem')

	## Finishing II
	hot_print_warna = fields.Char("Hot Print Warna",help="Isi field ini jika memilih 'Hot Print'")
	emboss_naik_turun = fields.Selection([('naik', 'Naik'), ('turun', 'Turun')],'Emboss Naik/Turun',help="Isi field ini jika memilih 'Emboss'")

	## Plong
	plong = fields.Selection([('putus', 'Putus'), ('half', '1/2 Putus'),('rit','Rit')],'Jenis Plong')

	## Finishing III
	potong_jadi_ket = fields.Text('Potong Jadi')
	fin_lain = fields.Text('Finishing Lain')

