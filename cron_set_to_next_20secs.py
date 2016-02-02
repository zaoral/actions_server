#  Your action should sty like this:
#  https://www.evernote.com/l/AJ5JbbEXaI5FMqZq-yRKnVz4sQcZ7X9AOpcB/image.png
object.write({'nextcall': (datetime.datetime.now() + dateutil.relativedelta.relativedelta(seconds=20)).strftime('%Y-%m-%d %H:%M:%S')})
