class brand_parser:
    def __init__(self,raw_data = None):
        self.raw_data = raw_data
    def run(self):
        # list of all devices that are currently supported
        brand_list = ['cisco','meraki','avaya','ise','air']
        brand_list = [x.lower() for x in brand_list]
        raw_desc =  [x.lower() for x in self.raw_data["system_description"].split(" ")]
        main_brand = [brand.lower() for brand in brand_list if brand in raw_desc]
        self.raw_data["brand"] = main_brand[0]
        return self.raw_data

