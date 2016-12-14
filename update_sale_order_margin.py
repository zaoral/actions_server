for sale in obj:
    old_value = sale.margin
    for line in sale.order_line:
        line.write({'purchase_price': line.purchase_price * 1.0})

    # Prepare log message
    subject = "Update/Fix Sale Order Margin server action has been run"
    msg = "<ul><li><b>Margin:</b> %(old)s &#8594; %(new)s </li></ul>" % dict(
            old=old_value, new=sale.margin)
    self.message_post(cr, uid, object.id, body=msg, type='comment',
                      subject=subject, subtype='html')
