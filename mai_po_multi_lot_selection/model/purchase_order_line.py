# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import Warning


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for picking_id in self.picking_ids:
            for move_id in picking_id.move_lines:
                for line in self.order_line:
                    if line == move_id.purchase_line_id:
                        move_id.set_serial_lot(line)
        return res


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    lot_ids = fields.Many2many('stock.production.lot', string='Lot', copy=False)


class StockMove(models.Model):
    _inherit = "stock.move"

    def set_serial_lot(self, line):
        if self.product_id.tracking == 'lot':
            lot_id = line.lot_ids[0]
            if self.move_line_ids:
                for move_line_id in self.move_line_ids:
                    move_line_id.write({
                        'lot_id': lot_id.id,
                        'lot_name': lot_id.name,
                        'product_uom_qty': line.product_qty,
                        'qty_done': line.product_qty, 
                        'product_uom_id': self.product_id.uom_id.id,
                        'location_id': self.location_id.id, 
                        'location_dest_id': self.location_dest_id.id})
            else:
                self.env['stock.move.line'].create({
                    'lot_id': lot_id.id,
                    'lot_name': lot_id.name,
                    'product_uom_qty': line.product_qty,
                    'qty_done': line.product_qty,
                    'product_uom_id': self.product_id.uom_id.id,
                    'location_id': self.location_id.id,
                    'location_dest_id': self.location_dest_id.id,
                    'move_id': self.id,
                    'product_id': self.product_id.id
                })
        elif self.product_id.tracking == 'serial':
            if len(line.lot_ids) != line.product_qty:
                raise Warning(_('Serial not defined in Lot as per Quantity!'))
            if self.move_line_ids:
                index = 0
                for move_line_id in self.move_line_ids:
                    lot_id = line.lot_ids[index]
                    move_line_id.write({
                        'lot_id': lot_id.id,
                        'lot_name': lot_id.name,
                        'product_uom_qty': 1,
                        'qty_done': 1,
                        'product_uom_id': self.product_id.uom_id.id,
                        'location_id': self.location_id.id, 
                        'location_dest_id': self.location_dest_id.id
                    })
                    index += 1
            else:
                SML_obj =self.env['stock.move.line']
                for lot_id in self.lot_ids:
                    SML_obj.create({
                       'lot_id': lot_id.id,
                       'lot_name': lot_id.name,
                       'product_uom_qty':1.0,
                       'qty_done':1.0,
                       'product_uom_id':self.product_id.uom_id.id,
                       'location_id': self.location_id.id,
                       'location_dest_id': self.location_dest_id.id,
                       'move_id': self.id,
                       'product_id': self.product_id.id
                    })