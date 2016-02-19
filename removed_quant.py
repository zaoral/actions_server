"""This action server removed negative quants when this quants was created by 'Moviento extra' in transfer of picking out and the
    stock.move was invoiced, this action sever does:
        1.- Break reconciliation of stock move by Movimiento extra
        2.- Deleted journal items created by stock move by Movimiento extra
        3.- Related account.move.line created by invoice with stock.move that did not negative quant
        4.- Remove quants created by Movimiento extra stock.move
"""

for move in model.browse(context.get('active_ids')):
    if 'Movimiento extra' in move.name:
        move.quant_ids.with_context({'force_unlink': True}).unlink()
        move_extra_id = move.aml_all_ids.filtered(lambda dat: dat.journal_id.type == 'general')
        move_extra_inv_id = move.aml_all_ids.filtered(lambda dat: dat.journal_id.type != 'general')
        self.pool.get('account.move.line')._remove_move_reconcile(cr, uid, [move_id.id for move_id in move.aml_all_ids])
        move_extra_id.unlink()
    else:
        move_src_id = move.id
move_extra_inv_id.write({'sm_id': move_src_id})
