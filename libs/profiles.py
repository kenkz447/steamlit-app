from libs.scanner import ScannerProfile

class BDSProfile(ScannerProfile):
    url = None
    fields = {
        "name": "#fix-body > div.container > div > div > div > div.group-infor-member > div > div > span.member-name-info",
        "mobile": "#fix-body > div.container > div > div > div > div.group-infor-member > div > div > h2 > a"
    }

    def __init__(self, id: int):
        self.url = f"https://bds.com.vn/thanh-vien-{id}.html"

    def check_status(self, page):
        try:
            page.query_selector("#fix-body > div.container > div > div > div > div.group-infor-member > div > div > span.member-name-info").inner_text()
        except Exception as e:
            raise  Exception("No data found")

    def before_select(self, page):
        pass

class BanNha888Profile(ScannerProfile):
    url = None
    fields = {
        "name": "#divSearchPage",
        "mobile": "#mm-0 > div:nth-child(2) > article > section > div.conten > div.pagewrap.page_conten_page > div.left_conten > div > div > div > div > center > div.trangcanhan-info > p:nth-child(2) > a > span"
    }

    def __init__(self, id: int):
        self.url = f"https://bannha888.com/thanh-vien/{id}"

    def check_status(self, page):
        try:
            page.query_selector("#mm-0 > div:nth-child(2) > article > section > div.conten > div.pagewrap.page_conten_page > div.left_conten > div > div > div > div > center > div.trangcanhan-info > p:nth-child(2) > a > span").inner_text()
        except Exception as e:
            raise  Exception("No data found")
        
    def before_select(self, page):
        page.click("#mm-0 > div:nth-child(2) > article > section > div.conten > div.pagewrap.page_conten_page > div.left_conten > div > div > div > div > center > div.trangcanhan-info > p:nth-child(2) > a")
        pass

class NhaDatCafeLandVnProfile(ScannerProfile):
    url = None
    fields = {
        "name": "body > div:nth-child(5) > div > div.moigioi-infor > div.moigioi-fullname",
        "mobile": "#detailTelSpan"
    }

    def __init__(self, id: int):
        self.url = f"https://nhadat.cafeland.vn/moi-gioi/khang-tho-dia-0911911021-{id}.html"

    def check_status(self, page):
        try:
            page.query_selector(self.fields.get("name")).inner_text()
        except Exception as e:
            raise  Exception("No data found")
        
    def before_select(self, page):
        page.click(self.fields.get("mobile"))
        pass

class NhaDat24hProfile(ScannerProfile):
    url = None
    fields = {
        "name": "#divSearchPage",
        "mobile": "#content > div > div.ct-in-l > div > div > div:nth-child(1) > center > div.trangcanhan-info > p:nth-child(1) > a"
    }

    def __init__(self, id: int):
        self.url = f"https://nhadat24h.net/tv/{id}"

    def check_status(self, page):
        try:
            page.query_selector(self.fields.get("name")).inner_text()
        except Exception as e:
            raise  Exception("No data found")

    def before_select(self, page):
        pass

class MogiProfile(ScannerProfile):
    url = None
    fields = {
        "name": "#agent > div.info > h1",
        "mobile": "#agent > div.info > div.agent-phone > a"
    }

    def __init__(self, id: int):
        self.url = f"https://mogi.vn/moi-gioi/0834982539-truong-an-uid{id}"

    def check_status(self, page):
        try:
            page.query_selector(self.fields.get("name")).inner_text()
        except Exception as e:
            raise  Exception("No data found")

    def before_select(self, page):
        pass

def select_profile(site:str, id: int):
    if site == "bds.com.vn":
        return BDSProfile(id)
    elif site == "bannha888":
        return BanNha888Profile(id)
    elif site == "nhadat.cafeland.vn":
        return NhaDatCafeLandVnProfile(id)
    elif site == "nhadat24h.net":
        return NhaDat24hProfile(id)
    elif site == "mogi.vn":
        return MogiProfile(id)
    return None