# Only used to run spiders from terminal

BOT_NAME = 'wine_sales_bot'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ITEM_PIPELINES = {
   'pipelines.SavingToDatabasePipeline': 300,
}
