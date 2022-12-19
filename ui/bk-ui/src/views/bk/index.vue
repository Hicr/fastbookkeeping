<template>
  <div class="demo">
    <el-container class="demoContainer">
      <el-header>
        <div class="bk-head">
          <a style="float:left;" class="tooher" @click="tosc">统计</a>
          <a class="jumptitle">快速记账</a>
          <el-button type="primary" plain style="float:right;margin-top: 10px;" @click="loginDialogVisible = true" v-show="!this.userid">登录</el-button>
          <a v-show="this.userid" class="userinfo" @click="logout">{{this.userid}}</a>
        </div>
      </el-header>
      <el-main>
        <div class="demoMain">
          <div class="bk-top">
            <el-card>
              <el-row  type="flex"  justify="space-between">
                <el-col :span="6">
                  <div>
                    <el-statistic group-separator="," :precision="2" :value="todymoneynum" :title="todymoneytitle" class="bk-font"></el-statistic>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div>
                    <el-statistic group-separator="," :precision="2" :value="contrasnum" :title="contrasttitle" class="bk-font">
                      <template slot="prefix">
                        <i v-if="showicon('minus')" class="el-icon-minus" style="color: black"></i>
                        <i v-if="showicon('top')" class="el-icon-top" style="color: red"></i>
                        <i v-if="showicon('bottom')" class="el-icon-bottom" style="color: green"></i>
                      </template>
                    </el-statistic>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div>
                    <el-statistic group-separator="," :precision="2" :value="mouthmoneynum" :title="mouthmoneytitle" class="bk-font"></el-statistic>
                  </div>
                </el-col>
              </el-row>
            </el-card>
          </div>
          <div class="bk-main">
            <el-card style=" margin-top: 5px;">
              <div slot="header" class="clearfix">
                <i class="el-icon-collection-tag" style="color: orange"></i>
                <span class="bk-font">速记</span>
              </div>
              <el-tag
                v-for="tag in moneyTags"
                :key="tag.value"
                style="margin: 3px;"
                @click="tagssubmit(tag.value)"
                :type="tag.color">
                {{tag.label}}
              </el-tag>
            </el-card>
            <el-card style=" margin-top: 5px;">
              <el-select v-model="type" placeholder="请选择消费类型" style="width:100%">
                <el-option
                  v-for="item in types"
                  :key="item.label"
                  :label="item.label"
                  :value="item.label">
                </el-option>
              </el-select>
              <el-input v-model="desc" placeholder="请输入消费描述" style=" margin-top: 10px;"></el-input>
              <el-input v-model="money" placeholder="请输入消费金额" style=" margin-top: 10px;" oninput="value=value.replace(/^\.+|[^\d.]/g,'')" @blur="salaryChange"></el-input>
              <!--   TODO 补填           -->
              <el-row   style="margin-top: 10px;" :gutter="20">
                <el-col :span="6">
                  <el-button @click="restForm" :loading="submitloading">重 置</el-button>
                </el-col>
                <el-col :span="6">
                  <el-button type="primary" @click="submitForm" :loading="submitloading">提 交</el-button>
                </el-col>
                <el-col :span="6">
                  <el-button type="primary" @click="opendaysubmit" :loading="submitloading">指定时间提交</el-button>
                </el-col>
              </el-row>
            </el-card>
          </div>
          <div class="bk-foot">

            <el-card style=" margin-top: 5px;">
              <div slot="header" class="clearfix">
                <i class="el-icon-shopping-bag-2" style="color: orange"></i>
                <span class="bk-font">今日消费明细</span>
              </div>
              <div v-show="!moneyemptyStatus">
                <el-row :gutter="20">
                  <el-col :span="6"><a class="bk-font">发生日期</a></el-col>
                  <el-col :span="6"><a class="bk-font">消费类别</a></el-col>
                  <el-col :span="6"><a class="bk-font">消费内容</a></el-col>
                  <el-col :span="6"><a class="bk-font">消费金额</a></el-col>
                </el-row>
                <br>
                <div v-for="item in todyMoneyListDatas">
                  <el-row :gutter="20">
                    <el-col :span="6">{{item.today}}</el-col>
                    <el-col :span="6">{{item.type}}</el-col>
                    <el-col :span="6">{{item.desc}}</el-col>
                    <el-col :span="6">{{item.money}}</el-col>
                  </el-row>
                  <br>
                </div>
<!--                <el-table-->
<!--                  :data="todyMoneyListDatas"-->
<!--                  @row-dblclick="dblclick"-->
<!--                  style="width: 100%">-->
<!--                  <el-table-column-->
<!--                    prop="today"-->
<!--                    label="时间"-->
<!--                    width="60">-->
<!--                  </el-table-column>-->
<!--                  <el-table-column-->
<!--                    prop="type"-->
<!--                    label="类别"-->
<!--                    width="80">-->
<!--                  </el-table-column>-->
<!--                  <el-table-column-->
<!--                    prop="desc"-->
<!--                    width="100"-->
<!--                    label="内容">-->
<!--                  </el-table-column>-->
<!--                  <el-table-column-->
<!--                    prop="money"-->
<!--                    label="金额">-->
<!--                  </el-table-column>-->
<!--                  <el-table-column-->
<!--                    prop="operate"-->
<!--                    width="50"-->
<!--                    label="操作">-->
<!--                    <template slot-scope="{row}">-->
<!--                      <el-button>-->
<!--                        删除-->
<!--                      </el-button>-->
<!--                    </template>-->
<!--                  </el-table-column>-->
                </el-table>
              </div>
              <el-empty description="今日无消费" v-show="moneyemptyStatus"></el-empty>
            </el-card>
          </div>
        </div>
      </el-main>
    </el-container>
    <el-dialog
      title="登 录"
      :visible.sync="loginDialogVisible"
      width="90%"
      center>
      <div>
        <el-form label-position="right" label-width="80px" :model="form">
          <el-form-item label="用户名">
            <el-input v-model="form.username"  placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码">
            <el-input v-model="form.pwd" show-password placeholder="请输入密码"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelLogin">取 消</el-button>
        <el-button type="primary" @click="login">登 录</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="请选择补填时间"
      :visible.sync="daydialog"
      width="90%"
      :before-close="canceldaysubmit">
      <el-date-picker
        v-model="dayTime"
        size="small"
        align="center"
        type="date"
        placeholder="选择日期"
        :picker-options="pickerOptions"
        value-format="yyyy-MM-dd">
      </el-date-picker>
      <br>
      <span slot="footer" class="dialog-footer">
    <el-button @click="canceldaysubmit">取 消</el-button>
    <el-button type="primary" @click="daysumbit">确 定</el-button>
  </span>
    </el-dialog>
  </div>
</template>

<script>
const qs = require('qs') //引入序列化功能
export default {
  name: 'bk',
  components: {},
  props: {},
  data() {
    return {
      IP:'http://127.0.0.1:9988',
      daydialog:false,// 补填窗口控制
      dayTime:'',
      submitloading:false,//提交加载控制
      moneyemptyStatus:true,// 是否显示为空
      loginDialogVisible:false,
      todymoneytitle:'今日花销',
      todymoneynum:0,// 本日花费
      mouthmoneytitle:'本月花销',
      mouthmoneynum:0,// 本月花费总额
      contrasttitle:'昨日对比',
      contrasnum:0,//昨日对比数量
      contraStats:3,//对比状态，1正，0负,2平
      type:'',// 类型
      userid:'',// 当前用户
      money:'',//金额
      desc:'',// 描述
      form: {
        username:'',
        pwd:''
      },
      types:[
        {label:'交通'},{label:'购物'},{label:'生活'},{label:'社交'},{label:'饮食'}
      ],
      moneyTags:[
        {label:'早餐 8元',value:'饮食/早餐/8',color:''},
        {label:'交通 15元',value:'交通/交通/15',color:''},
        {label:'交通 9元',value:'交通/交通/9',color:''},
        {label:'午餐 14元',value:'饮食/午餐/14',color:''},
      ],
      todyMoneyListDatas:[],// 今日账单列表信息
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now();
        },
      },

    }
  },
  computed: {},
  watch: {},
  created() {},
  mounted() {
    this.userid = localStorage.getItem('userid')
    this.loading()
  },
  methods: {
    staticloading(){
      // 查询统计值
      if(this.online()){
        this.$request
          .post(this.IP + '/ylbk/statistics' + '?userid=' + this.userid)
          .then((res) => {
            console.log(res)
            if(res.data.code === 200){
              this.todymoneynum = res.data.data.todaySum
              this.mouthmoneynum = res.data.data.tmSum
              this.contrasnum = res.data.data.dSum
              this.contraStats = res.data.data.stats
            }else{
              // this.$message.error('查询失败');
              console.log('查询失败')
            }
          })
          .catch((err) => console.log(err))
      }else{
        this.outline()
      }
    },
    showicon(stats){
      if(this.contraStats == 0 && stats === 'bottom'){
        return true
      }else if(this.contraStats == 1 && stats === 'top'){
        return true
      }else if(this.contraStats == 2 && stats === 'minus'){
        return true
      }else if(this.contraStats == 3 && stats === 'minus'){
        return true
      }else {
        return false
      }
    },
    // 加载今日账单
    todyMoneyList(){
      if (this.online()){
        // 有数据 显示 无数据显示空面板
        this.$request
          .post(this.IP + '/ylbk/querybkToday' + '?userid=' + this.userid)
          .then((res) => {
            console.log(res)
            if(res.data.code === 200){
              this.todyMoneyListDatas = []
              this.todyMoneyListDatas = res.data.data
              if(this.todyMoneyListDatas){
                this.moneyemptyStatus = false
              }

            }else{
              // this.$message.error('查询失败');
              console.log('查询失败')
            }
          })
          .catch((err) => console.log(err))
      }else{
        // 未登录
        this.moneyemptyStatus = true
      }
      this.$forceUpdate();
    },
    // 登录
    login(){
      if(this.form.username && this.form.pwd){
        this.$request
          .post(this.IP + '/ylbk/login' + '?username=' + this.form.username + '&pwd=' + this.form.pwd)
          .then((res) => {
            console.log(res)
            if(res.data.code === 200){
              // 将用户信息存入浏览器
              localStorage.setItem('userid',res.data.data)
              this.userid = localStorage.getItem('userid')
              this.loading()
              this.loginDialogVisible = false
              this.$message({
                message: '登录成功',
                duration: 1500,
                showClose: true,
                type: 'success'
              });
            }else{
              // this.$message.error('登陆失败');
              this.$message({
                message: '登陆失败',
                duration: 1500,
                showClose: true,
                type: 'error'
              });
            }
          })
          .catch((err) => console.log(err))
      }else{
        // this.$message.error('请完输入完整账号信息');
        this.$message({
          message: '请完输入完整账号信息',
          duration: 1500,
          showClose: true,
          type: 'error'
        });
      }
      this.restLoginForm()
    },
    restLoginForm(){
      this.form.pwd = ''
      this.form.username = ''
    },
    // 重置登录
    cancelLogin(){
      this.form.pwd = ''
      this.form.username = ''
      this.loginDialogVisible = false
    },
    // 提交记账
    submitForm(){
      this.submitloading = true
      if(this.online() ){
        if(this.validateMoney()){
          if (this.type && this.money && this.desc && this.userid){
            this.$request
              .post(this.IP + '/ylbk/bookkeeping' + '?userid=' + this.userid + '&type=' + this.type + '&desc=' + this.desc + '&money=' + this.money)
              .then((res) => {
                console.log(res)
                if(res.data.code === 200){
                  this.$message({
                    duration: 1500,
                    showClose: true,
                    message: '记账成功',
                    type: 'success'
                  });
                  this.restForm()
                }else{
                  // this.$message.error('发送异常');
                  this.$message({
                    message: '发送异常',
                    duration: 1500,
                    showClose: true,
                    type: 'error'
                  });
                }
                this.submitloading = false
              })
              .catch((err) => console.log(err),this.submitloading = false)
          }else{
            this.submitloading = false
            // this.$message.error('缺少提交信息');
            this.$message({
              message: '缺少提交信息',
              duration: 1500,
              showClose: true,
              type: 'error'
            });
          }
          this.loading()
        }else {
          this.submitloading = false
          // this.$message.error('消费金额格式有误');
          this.$message({
            message: '消费金额格式有误',
            duration: 1500,
            showClose: true,
            type: 'error'
          });
        }
      }else {
        this.submitloading = false
        this.outline()
      }

    },
    // 重置记账
    restForm(){
      this.submitloading = true
      this.type = ''
      this.money = ''
      this.desc = ''
      this.submitloading = false
      this.loading()
    },
    // 标签速记
    tagssubmit(value){
      if(this.online()){
        this.$confirm('请确认消费?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          var values = value.split('/')
          var tagtype = values[0]
          var tagdesc = values[1]
          var tagmoney = values[2]
          this.$request
            .post(this.IP +  '/ylbk/bookkeeping' + '?userid=' + this.userid + '&type=' + tagtype + '&desc=' + tagdesc + '&money=' + tagmoney)
            .then((res) => {
              console.log(res)
              if(res.data.code === 200){
                this.$message({
                  duration: 1500,
                  showClose: true,
                  message: '记账成功',
                  type: 'success'
                });
                this.restForm()
                this.loading()
              }else{
                // this.$message.error('记账异常');
                this.$message({
                  message: '记账异常',
                  duration: 1500,
                  showClose: true,
                  type: 'error'
                });
              }
              this.submitloading = false

            })
            .catch((err) => console.log(err),this.submitloading = false)
        }).catch(() => {
          this.$message({
            duration: 1500,
            showClose: true,
            type: 'info',
            message: '已取消记账'
          });
        });
      }else{
        this.outline()
      }
    },
    online(){
      if (this.userid){
        return true
      }else {
        return false
      }
    },
    outline(){
      // this.$message('请先登录');
      this.$message({
        message: '请先登录',
        duration: 1500,
        showClose: true,
        type: 'info'
      });
    },
    loading(){
      this.staticloading()
      this.todyMoneyList()
    },
    salaryChange(e){
      this.money = e.target.value
    },
    validateMoney(){
      if(this.money){
        var val_moneys = this.money.split('.')
        if(val_moneys.length>2){
          return false
        }else {
          return true
        }
      }
    },
    logout(){
      this.$confirm('是否退出登录?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        localStorage.removeItem('userid')
        this.clear()
        this.$message({
          duration: 1500,
          showClose: true,
          type: 'success',
          message: '已退出登录!'
        });
      }).catch(() => {
        this.$message({
          duration: 1500,
          showClose: true,
          type: 'info',
          message: '已取消'
        });
      });
    },
    clear(){
      this.todymoneynum=0,
        this.mouthmoneynum=0,
        this.contrasnum=0,
        this.contraStats=0,
        this.type='',
        this.userid='',
        this.money='',
        this.desc='',
        this.todyMoneyListDatas = []
      this.moneyemptyStatus = true
    },
    tosc(){
      this.$router.push('/sc')
    },
    // 打开弹窗
    opendaysubmit(){
      if(this.online()){
        this.daydialog = true
      }else{
        this.outline()
      }
    },
    // 关闭弹窗
    canceldaysubmit(){
      this.dayTime = ''
      this.daydialog = false
    },
    // 提交方法
    daysumbit(){
      console.log(this.dayTime)
      this.submitloading = true
      if(this.online() ){
        if(this.validateMoney()){
          if (this.type && this.money && this.desc && this.userid){
            this.$request
              .post(this.IP + '/ylbk/bookkeeping' + '?userid=' + this.userid + '&type=' + this.type + '&desc=' + this.desc + '&money=' + this.money + '&day=' + this.dayTime)
              .then((res) => {
                console.log(res)
                if(res.data.code === 200){
                  this.$message({
                    duration: 1500,
                    showClose: true,
                    message: '记账成功',
                    type: 'success'
                  });
                  this.restForm()
                  this.canceldaysubmit()
                }else{
                  // this.$message.error('发送异常');
                  this.$message({
                    message: '发送异常',
                    duration: 1500,
                    showClose: true,
                    type: 'error'
                  });
                }
                this.submitloading = false
              })
              .catch((err) => console.log(err),this.submitloading = false)
          }else{
            this.submitloading = false
            // this.$message.error('缺少提交信息');
            this.$message({
              message: '缺少提交信息',
              duration: 1500,
              showClose: true,
              type: 'error'
            });
          }
          this.loading()
        }else {
          this.submitloading = false
          // this.$message.error('消费金额格式有误');
          this.$message({
            message: '消费金额格式有误',
            duration: 1500,
            showClose: true,
            type: 'error'
          });
        }
      }else {
        this.submitloading = false
        this.outline()
      }
    },
    dblclick(row){
      console.log(row)
    }
  },
}
</script>
<style lang="css" scoped>
.bk-head{

}
.bk-top{

}
.bk-main{
  margin-top: 5px;
}
.bk-foot{
  margin-top: 5px;
}
.bk-font{
  font-family: '微软雅黑';
  color: #333;
  font-weight: bold;
}
.bk-message{
  width: 50%;
  margin: 10px;
}
/deep/ .el-message-box{
  width: 220px;
}
.userinfo{
  float:right;
  /*margin-top: 1px;*/
  font-family: '微软雅黑';
  color: #333;
  font-size: larger;
  font-weight: 800;
}
.demo {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.demoContainer {
  height: 100%;
}
.el-header,
.el-footer {
  background-color: #f89b11;
  color: #333;
  text-align: center;
  line-height: 60px;
}
.el-main {
  background-color: #e9eef3;
  color: #333;
  /* text-align: center; */
  /* line-height: 160px; */
}
.demoMain {
  /*margin-left: 200px;*/
  width: 100%;

}
.tooher{
  font-family: '微软雅黑';
  color: #333;
  font-weight: bold;
  font-size: large;
}
.demoOperation {
  margin-bottom: 10px;
}
.jumptitle {
  font-family: '微软雅黑';
  color: #333;
  font-size: larger;
  font-weight: 800;
}
</style>
<style>
.el-message-box{
  width: 220px;
}
</style>
