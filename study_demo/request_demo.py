import requests
import pandas_demo
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class LoginUser:
    def __init__(self, userAcct, password):
        self.userAcct = userAcct
        self.password = password

# 获取token
def get_token():
    wmy = LoginUser(userAcct="80000001", password="80000001@0031")
    lf = LoginUser(userAcct="80003602", password="123456")
    hc = LoginUser(userAcct="80000056", password="80000056@1547")
    yj = LoginUser(userAcct="80002254", password="80002254@2071")
    cd = LoginUser(userAcct="80000141", password="80000141@8508")
    yy = LoginUser(userAcct="80000140", password="80000140@3972")
    gxq = LoginUser(userAcct="80001246", password="80001246@0709")
    lff = LoginUser(userAcct="80000087", password="80000087@7925")
    lxf = LoginUser(userAcct="80005014", password="18684891128@1128")
    loginUser = lff
    url = "https://sso.jiayihn.com/api/auth/oauth2/login"
    params = {
        'userAcct': loginUser.userAcct,
        'password': loginUser.password
    }
    response = requests.post(url, params=params, verify=False) # verify=False表示忽略SSL证书验证
    print(f"请求结果:{response.text}")

def submit_point() -> None:
    url = "https://qywork.jiayihn.com/api/work/locasys-task-collect/point-submit"
    request_body = {"activeLine":1,"advantagesDescription":"","auditResult":1,"averageMonthlySalesEstimate":7000.00,"averageMonthlySalesEstimateWithoutSmoke":5000.00,"beforeFlipBrand":"","brokerageFee":0.00,"canTobaccoLicence":1,"collectType":"POINT_UPDATE","contactPersonName":"肖总","contactPersonPosition":"房东","contactPhone":"18692962665","cornerShop":1,"custAttrs":[{"coverageRate":70.00,"customerGroup":"居住人口","customerType":"社区居住人口","footfallRate":5.00,"occupancyRate":90.00,"totalCount":8000}],"disadvantagesDescription":"","districtId":1349123103808626688,"doorStepNum":"无台阶","draftId":0,"entranceFee":0.00,"existCompetitor":[{"name":"无品牌","num":1}],"existCompetitorStr":"[{\"name\":\"无品牌\",\"num\":1}]","firstMonthSalesEstimate":5500.00,"firstMonthSalesEstimateWithoutSmoke":4200.00,"flip":0,"hasCompetitor":1,"headShop":0,"houseNumber":"1","images":[{"fileType":"1","id":92998,"url":"https://xjy-public-1320028207.cos.ap-guangzhou.myqcloud.com/e049ba0eef7943b7953441a00129eb72_960x1280.jpg","visualType":1},{"fileType":"1","id":92999,"url":"https://xjy-public-1320028207.cos.ap-guangzhou.myqcloud.com/51f656847da34d169cfa54fe4f9a2aee_960x1280.jpg","visualType":3},{"fileType":"1","id":93000,"url":"https://xjy-public-1320028207.cos.ap-guangzhou.myqcloud.com/ca3109f8f1324b34852d26058dbd5988_960x1280.jpg","visualType":2}],"incubationPeriod":2,"laneNum":"无车道","leaseDeposit":0.00,"leaseMinimumTerm":5,"locationType":"社区立地","meetCriteria":["给水","排水","外机位","招牌位","电容(35KW)"],"meetCriteriaStr":"[\"给水\",\"排水\",\"外机位\",\"招牌位\",\"电容(35KW)\"]","memberCode":"614084443","monthlyProfitAmount":8905.67,"outsideTradeType":"外","pointAddress":"邵阳市绿景盛世豪庭(梨园中路)","pointId":12121,"pointName":"洞口钓鱼岛购物中心","pointSituation":"便利店","ponitLatitude":"27.047566","ponitLongitude":"110.589587","remark":"","rent":5000.00,"rentIncreaseRate":0.00,"rentPayCycle":"季度付","rentPayType":"押一付三","retailFloorArea":100.00,"roadMedianStrip":0,"shopkeeperGender":"男","shopkeeperIntention":"","shopkeeperLevel":"","signLength":9.00,"storefrontNature":"自购","taskCode":"1372483654478675968","tradeLabel":[{"name":"居住场所(住宅)","main":1,"selectedValue":["住宅小区"]},{"name":"住宿服务","main":0,"selectedValue":["酒店"]}],"tradeLabelStr":"[{\"name\":\"居住场所(住宅)\",\"main\":1,\"selectedValue\":[\"住宅小区\"]},{\"name\":\"住宿服务\",\"main\":0,\"selectedValue\":[\"酒店\"]}]","videos":[{"fileType":"2","id":93001,"url":"https://xjy-public-1320028207.cos.ap-guangzhou.myqcloud.com/c52a696143c9439ab21bf119ed64c8f7.mp4","visualType":5}],"xjy200Name":"","xjyNearM200":0}
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJtZW1iZXJDb2RlIjoiNjE0MDg0NDQzIiwiZXhwIjoxNzUzOTI5NDE2LCJpYXQiOjE3NTM5MjIyMTZ9.XGkSuuGON2MLvLZxcv-gAu3fBXywdvqHMWEx-Lfz60Q'
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.post(url, headers=headers, json=request_body, verify=False) # verify=False表示忽略SSL证书验证
    print(f"响应：{response.text}")


if __name__ == "__main__":
    print("start!")

    get_token()