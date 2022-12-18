<template>
  <div class="demo">
    <el-container class="demoContainer">
      <el-header>
        <div class="bk-head">
          <a style="float:left;" class="tooher" @click="tobk">记账</a>
          <a class="jumptitle">开销统计</a>
          <el-button type="primary" plain style="float:right;margin-top: 10px;" @click="loginDialogVisible = true" v-show="!this.userid">登录</el-button>
          <a v-show="this.userid" class="userinfo" @click="logout">{{this.userid}}</a>
        </div>
      </el-header>
      <el-main>
        <div class="demoMain">

          <div class="bk-main">
            <el-card>
              <div slot="header" class="clearfix">
                <span class="sc-font">日开销分类统计</span>
                <el-date-picker
                  style="float: right;width: 150px"
                  v-model="d1"
                  size="small"
                  align="right"
                  type="date"
                  placeholder="选择日期"
                  value-format="yyyy-MM-dd">
                </el-date-picker>
              </div>
              <div>
                <dChart v-if="!d1state" id="d1highcharts" ref="d1" class="high" :option="d1option"></dChart>
                <el-empty description="无统计数据" v-if="d1state"></el-empty>
              </div>
            </el-card>

            <el-card style=" margin-top: 5px;">
              <div slot="header" class="clearfix">
                <span class="sc-font">月开销分类统计</span>
                <el-date-picker
                  style="float: right;width: 150px"
                  v-model="m1"
                  size="small"
                  type="month"
                  placeholder="选择月"
                  value-format="yyyy-MM">
                </el-date-picker>
              </div>
              <div>
                <dChart v-if="!m1state" id="m1highcharts" ref="m1" class="high" :option="m1option"></dChart>
                <el-empty description="无统计数据" v-if="m1state"></el-empty>
              </div>
            </el-card>
            <el-card style=" margin-top: 5px;">
              <div slot="header" class="clearfix">
                <span class="sc-font">月开销明细统计</span>
                <el-date-picker
                  style="float: right;width: 150px"
                  v-model="m2"
                  size="small"
                  type="month"
                  placeholder="选择月"
                  value-format="yyyy-MM">
                </el-date-picker>
              </div>
              <div>
                <dChart v-if="!m2state" id="m2highcharts" ref="m2" class="high" :option="m2option"></dChart>
                <el-empty description="无统计数据" v-if="m2state"></el-empty>
              </div>
            </el-card>
            <el-card style=" margin-top: 5px;">
              <div slot="header" class="clearfix">
                <span class="sc-font">月消费曲线</span>
                <el-date-picker
                  style="float: right;width: 150px"
                  v-model="m3"
                  size="small"
                  type="month"
                  placeholder="选择月"
                  value-format="yyyy-MM">
                </el-date-picker>
              </div>
              <div>
                <dChart v-if="!m3state" id="m3highcharts" class="high" ref="m3" :option="m3option"></dChart>
                <el-empty description="无统计数据" v-if="m3state"></el-empty>
              </div>
            </el-card>
            <el-card style=" margin-top: 5px;">
              <div slot="header" class="clearfix">
                <span class="sc-font">年消费曲线</span>
                <el-date-picker
                  style="float: right;width: 150px"
                  v-model="y1"
                  size="small"
                  type="year"
                  placeholder="选择年"
                  value-format="yyyy">
                </el-date-picker>
              </div>
              <div>
                <dChart v-if="!y1state"  id="y1highcharts" class="high" ref="y1" :option="y1option"></dChart>
                <el-empty description="无统计数据" v-if="y1state"></el-empty>
              </div>
            </el-card>
            <el-card style=" margin-top: 5px;">
              <div slot="header" class="clearfix">
                <span class="sc-font">消费词云</span>
                <el-date-picker
                  style="float: right;width: 150px"
                  v-model="y2"
                  size="small"
                  type="year"
                  placeholder="选择年"
                  value-format="yyyy">
                </el-date-picker>
              </div>
              <div>
                <yChart  v-if="!y2state" id="y2highcharts" class="high" ref="y2"  :option="y2option"></yChart>
                <el-empty description="无统计数据" v-if="y2state"></el-empty>
              </div>
            </el-card>
          </div>
          <div class="bk-foot">

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
  </div>
</template>
<script>
const qs = require('qs') //引入序列化功能
import dChart from '@/components/charts_day'
// 词云图
import yChart from '@/components/charts_year'
export default {
  name: 'statistics',
  components: {dChart,yChart},
  props: {},
  data() {
    return {
      IP:'http://127.0.0.1:9988',
      loginDialogVisible:false,
      d1state:true,
      m1state:true,
      m2state:true,
      m3state:true,
      y1state:true,
      y2state:true,
      d1:'',
      m1:'',
      m2:'',
      m3:'',
      y1:'',
      y2:'',
      form: {
        username:'',
        pwd:''
      },
      userid:'',
      d1charts:[],
      m1charts:[],
      m2charts:[],
      m3charts:[],
      m3cate:[],
      m3label:'',
      y1charts:[],
      y1cate:[],
      y1label:'',
      y2charts:[],
      d1option:{
        chart: {
          type: 'column'
        },
        credits:{
          enabled: false // 禁用版权信息
        },
        title: {
          text: ''
        },
        subtitle: {
          text: ''
        },
        xAxis: {
          type: 'category',
          labels: {
            rotation: 0  // 设置轴标签旋转角度
          }
        },
        yAxis: {
          min: 0,
          title: {
            text: '人民币 (元)'
          }
        },
        legend: {
          enabled: false
        },
        tooltip: {
          enabled: true,
          pointFormat: '<b>{point.y:.1f} 元</b>'
        },
        series: [{
          name: '当日总开销',
          color:'#9999FF',
          data: [],
          dataLabels: {
            enabled: true,
            rotation: -90,
            color: '#FFFFFF',
            align: 'right',
            format: '{point.y:.1f}元', // :.1f 为保留 1 位小数
            y: 10
          }
        }]},
      m1option:{
        chart: {
          type: 'column'
        },
        credits:{
          enabled: false // 禁用版权信息
        },
        title: {
          text: ''
        },
        subtitle: {
          text: ''
        },
        xAxis: {
          type: 'category',
          labels: {
            rotation: 0  // 设置轴标签旋转角度
          }
        },
        yAxis: {
          min: 0,
          title: {
            text: '人民币(元)'
          }
        },
        legend: {
          enabled: false
        },
        tooltip: {
          pointFormat: '<b>{point.y:.1f} 元</b>'
        },
        series: [{
          name: '当月总开销',
          color:'#9999FF',
          data: [

          ],
          dataLabels: {
            enabled: true,
            rotation: -90,
            color: '#FFFFFF',
            align: 'right',
            format: '{point.y:.1f}元', // :.1f 为保留 1 位小数
            y: 10
          }
        }]
      },
      m2option:{
        chart: {
          plotBackgroundColor: null,
          plotBorderWidth: null,
          plotShadow: false,
          type: 'pie'
        },
        credits:{
          enabled: false // 禁用版权信息
        },
        title: {
          text: ''
        },
        tooltip: {
          pointFormat: ''
        },
        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
              enabled: true,
              format: '<b>{point.name}</b>: {point.percentage:.1f} %',

            },
            showInLegend: false// 显示图例 就是图表下方说明
          }
        },
        series: [{
          name: '月消费分布',
          colorByPoint: true,
          data: []
        }]

      },
      m3option:{
        chart: {
          type: 'line'
        },
        credits:{
          enabled: false // 禁用版权信息
        },
        title: {
          text: ''
        },
        subtitle: {
          text: ''
        },
        xAxis: {
          categories: []
        },
        yAxis: {
          title: {
            text: '人民币(元)'
          }
        },
        plotOptions: {
          line: {
            dataLabels: {
              // 开启数据标签
              enabled: true
            },
            // 关闭鼠标跟踪，对应的提示框、点击事件会失效
            enableMouseTracking: true
          }
        },
        series: [{
          name: '',
          data: []
        },]
      },
      y1option:{
        chart: {
          type: 'line'
        },
        credits:{
          enabled: false // 禁用版权信息
        },
        title: {
          text: ''
        },
        subtitle: {
          text: ''
        },
        xAxis: {
          categories: []
        },
        yAxis: {
          title: {
            text: '人民币(元)'
          }
        },
        plotOptions: {
          line: {
            dataLabels: {
              // 开启数据标签
              enabled: true
            },
            // 关闭鼠标跟踪，对应的提示框、点击事件会失效
            enableMouseTracking: true
          }
        },
        series: [{
          name: '',
          data: []
        }]
      },
      y2option:{
        credits:{
          enabled: false // 禁用版权信息
        },
        series: [{
          type: 'wordcloud',
          data: []
        }],
        title: {
          text: ''
        }
      }
    }
  },
  computed: {},
  watch: {
    d1:{
      deep:true,
      handler(newVal,oldVal){
        if(this.online()){
          this.queryd1()
        }
      }
    },
    m1:{
      deep:true,
      handler(newVal,oldVal){
        if(this.online()){
          this.querym1()
        }
      }
    },
    m2:{
      deep:true,
      handler(newVal,oldVal){
        if(this.online()) {
          this.querym2()
        }
      }
    },
    m3:{
      deep:true,
      handler(newVal,oldVal){
        if(this.online()) {
          this.querym3()
        }
      }
    },
    y1:{
      deep:true,
      handler(newVal,oldVal){
        if(this.online()) {
          this.queryy1()
        }
      }
    },
    y2:{
      deep:true,
      handler(newVal,oldVal){
        if(this.online()) {
          this.queryy2()
        }
      }
    }

  },
  created() {
    this.userid = localStorage.getItem('userid')
    this.loading()
  },
  mounted() {


  },
  methods: {
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
              console.log(this.userid)
              this.loading()
              this.loginDialogVisible = false
              this.$message({
                message: '登录成功',
                type: 'success'
              });
            }else{
              this.$message.error('登陆失败');
            }
          })
          .catch((err) => console.log(err))
      }else{
        this.$message.error('请完输入完整账号信息');
      }
      this.restLoginForm()
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
          type: 'success',
          message: '已退出登录!'
        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消'
        });
      });
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
    async queryd1(){
      if(!this.d1){
        this.d1 = this.formData('day')
      }
      if(this.online()){
        this.d1charts = []
        this.d1option.series[0].data = []
        await this.$request
          .get(this.IP + '/ylsc/d1' + '?userid=' + this.userid + '&day=' + this.d1)
          .then((res) => {
            if(res.data.code === 200){
              this.d1charts = res.data.data
              if(this.d1charts && this.d1charts.length > 1){
                this.d1state = false
              }else{
                this.d1state = true
              }
              console.log(this.d1charts)
              this.d1option.series[0].data = this.d1charts
            }else{
              console.log('查询失败')
            }
          })
          .catch((err) => console.log(err))
      }else{
        this.outline()
      }
      this.$refs.d1.init()
    },
    async querym1(){
      if(!this.m1){
        this.m1 = this.formData('month')
      }
      if(this.online()){
        this.m1charts = []
        this.m1option.series[0].data = []
        await this.$request.get(this.IP + '/ylsc/m1' +  '?userid=' + this.userid + '&month=' + this.m1)
          .then((res) => {
            if(res.data.code === 200){
              this.m1charts = res.data.data
              if(this.m1charts && this.m1charts.length > 1){
                this.m1state = false
              }else{
                this.m1state = true
              }
              this.m1option.series[0].data = this.m1charts
            }else{
              console.log('查询失败')
            }
          }).catch((err) => console.log(err))
      }else{
        this.outline()
      }
      this.$refs.m1.init()
    },
    async querym2(){
      if(!this.m2){
        this.m2 = this.formData('month')
      }
      if(this.online()){
        this.m2charts = []
        this.m2option.series[0].data = []
        await this.$request.get(this.IP + '/ylsc/m2' +  '?userid=' + this.userid + '&month=' + this.m2)
          .then((res) => {
            if(res.data.code === 200){
              this.m2charts = res.data.data
              if(this.m2charts && this.m2charts.length > 1){
                this.m2state = false
              }else{
                this.m2state = true
              }
              this.m2option.series[0].data = this.m2charts
            }else{
              console.log('查询失败')
            }
          }).catch((err) => console.log(err))
      }else{
        this.outline()
      }
      this.$refs.m2.init()
    },
    async querym3(){
      if(!this.m3){
        this.m3 = this.formData('month')
      }
      if(this.online()){
        this.m3charts = []
        this.m3option.series[0].data = []
        this.m3option.series[0].name = ''
        this.m3option.xAxis.categories = ''
        await this.$request.get(this.IP + '/ylsc/m3' +  '?userid=' + this.userid + '&month=' + this.m3)
          .then((res) => {
            if(res.data.code === 200){
              if(res.data.data.charts || res.data.data.cata){
                this.m3charts = res.data.data.charts
                this.m3cate = res.data.data.cata
                this.m3state = false
                this.m3label = '消费'
                this.m3option.series[0].data = this.m3charts
                this.m3option.series[0].name = this.m3label
                this.m3option.xAxis.categories = this.m3cate
              }else{
                this.m3state = true
              }
            }else{
              console.log('查询失败')
              this.m3state = true
            }
          }).catch((err) => console.log(err))
      }else{
        this.outline()
      }
      this.$refs.m3.init()
    },
    async queryy1(){
      if(!this.y1){
        this.y1 = this.formData('year')
      }
      if(this.online()){
        this.y1charts = []
        this.y1option.series[0].data = []
        this.y1option.series[0].name = ''
        this.y1option.xAxis.categories = ''
        await this.$request.get(this.IP + '/ylsc/y1' +  '?userid=' + this.userid + '&year=' + this.y1)
          .then((res) => {
            if(res.data.code === 200){
              if(res.data.data.charts || res.data.data.cata){
                this.y1charts = res.data.data.charts
                this.y1cate = res.data.data.cata
                this.y1state = false
                this.y1label = '消费'
                this.y1option.series[0].data = this.y1charts
                this.y1option.series[0].name = this.y1label
                this.y1option.xAxis.categories = this.y1cate
              }else{
                this.y1state = true
              }
            }else{
              console.log('查询失败')
              this.y1state = true
            }
          }).catch((err) => console.log(err))
      }else{
        this.outline()
      }
      this.$refs.y1.init()
    },
    async queryy2(){
      if(!this.y2){
        this.y2 = this.formData('year')
      }
      if(this.online()){
        this.y2charts = []
        await this.$request.get(this.IP + '/ylsc/y2' +  '?userid=' + this.userid + '&year=' + this.y2)
          .then((res) => {
            if(res.data.code === 200){
              if(res.data.data){
                this.y2state = false
                this.y2charts = res.data.data
                this.y2option.series[0].data = this.y2charts
                console.log(this.y2option)
              }else{
                this.y2state = true
              }
            }else{
              console.log('查询失败')
              this.y2state = true
            }
          }).catch((err) => console.log(err))
      }else{
        this.outline()
      }
      this.$refs.y2.init()
    },
    loading(){
      if(this.online()){
        this.queryd1()
        this.querym1()
        this.querym2()
        this.querym3()
        this.queryy1()
        this.queryy2()
      }else{
        this.outline()
      }
    },
    clear(){
      this.userid = ''
      this.d1 = ''
      this.m1 = ''
      this.m2 = ''
      this.m3 = ''
      this.y1 = ''
      this.y2 = ''
      this.d1state=true
      this.m1state=true
      this.m2state=true
      this.m3state=true
      this.y1state=true
      this.y2state=true
      this.d1charts=[]
      this.m1charts=[]
      this.m2charts=[]
      this.m3charts=[]
      this.m3cate=[]
      this.m3label=''
      this.y1charts=[]
      this.y1cate=[]
      this.y1label=''
      this.y2charts=[]
      this.d1option.series[0].data = this.d1charts
      // this.$refs.d1.init()
      this.m1option.series[0].data = this.m1charts
      // this.$refs.m1.init()
      this.m2option.series[0].data = this.m2charts
      // this.$refs.m2.init()
      this.m3option.series[0].data = this.m3charts
      this.m3option.series[0].name = this.m3label
      this.m3option.xAxis.categories = this.m3cate
      // this.$refs.m3.init()
      this.y1option.series[0].data = this.y1charts
      this.y1option.series[0].name = this.y1label
      this.y1option.xAxis.categories = this.y1cate
      // this.$refs.y1.init()
    },
    formData(type){
      var myDate = new Date()
      var year = myDate.getFullYear()
      var month = myDate.getMonth() + 1;
      var day = myDate.getDate()
      month = (month > 9) ? month : ("0" + month);
      day = (day < 10) ? ("0" + day) : day;
      var today = year + "-" + month + "-" + day;
      var tomonth = year + '-' + month
      if(type === 'day'){
        return today
      }
      if(type === 'month'){
        return tomonth
      }
      if(type === 'year'){
        return year + ''
      }
      return null
    },
    online(){
      if(this.userid || localStorage.getItem('userid')){
        return true
      }else {
        return false
      }
    },
    outline(){
      this.$message('请先登录');
    },
    tobk(){
      this.$router.push('/')
    }
  }
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
.tooher{
  font-family: '微软雅黑';
  color: #333;
  font-weight: bold;
  font-size: large;
}
.sc-font{
  font-family: '微软雅黑';
  color: #333;
  font-weight: bold;
  font-size: large;
}
.bk-message{
  width: 50%;
  margin: 10px;
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
  background-color: #117df8;
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
.demoOperation {
  margin-bottom: 10px;
}
.jumptitle {
  font-family: '微软雅黑';
  color: #333;
  font-size: larger;
  font-weight: 800;
}
.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both
}
</style>
<style>
.el-message-box{
  width: 220px;
}
</style>
