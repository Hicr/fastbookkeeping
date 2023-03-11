const FB_TYPE = [
  {label:'交通'},{label:'购物'},{label:'生活'},{label:'饮食'},{label:'宠物'},{label:'游戏'}
]

const FB_TAGS = [
  {label:'早餐 8元',value:'饮食/早餐/8',color:''},
  {label:'打车 15元',value:'交通/打车/15',color:''},
  {label:'打车 9元',value:'交通/打车/9',color:''},
  {label:'话费 200元',value:'生活/话费/200',color:''},
  {label:'交通卡 100元',value:'交通/地铁卡/100',color:''}
]

const APP_LIST = [{
  label:'上海交通卡',value:'http://mobile.sptcc.com/event/?from=timeline&isappinstalled=1',type:''
},{
  label:'支付宝',value:'alipays://',type:''
},{
  label:'微信',value:'weixin://',type:'success'
},{
  label:'饿了么',value:'eleme://',type:''
},{
  label:'美团',value:'imeituan://',type:'warning'
},{
  label:'滴滴打车',value:'diditaxi://',type:'warning'
},{
  label:'淘宝',value:'taobao://',type:'danger'
},{
  label:'京东',value:'openApp.jdMobile://',type:'danger'
},{
  label:'拼多多',value:'pinduoduo://',type:'danger'
},]

export {
  FB_TYPE,FB_TAGS,APP_LIST
}
