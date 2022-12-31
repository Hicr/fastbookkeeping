<template>
  <div class="demo">
    <el-container class="demoContainer">
      <el-header>
        <div class="bk-head">
          <a style="float:left;" class="tooher" @click="tobk">记 账</a>
          <a style="float:left;margin-left: 10px;" class="tooher" >|</a>
          <a style="float:left;margin-left: 10px;" class="tooher" @click="tosc">统 计</a>
          <a style="float:left;margin-left: 10px;" class="tooher" v-show="this.userid">|</a>
          <a style="float:left;margin-left: 10px;" v-show="this.userid" class="tooher" @click="logout">退 出</a>
          <a class="jumptitle">账单统计</a>
          <el-button type="primary" plain style="float:right;margin-top: 10px;" @click="loginDialogVisible = true" v-show="!this.userid">登 录</el-button>
          <a v-show="this.userid" class="userinfo" @click="logout">{{this.userid}}</a>
        </div>
      </el-header>
      <el-main>
        <div class="demoMain">
          <el-card>
            <div slot="header" class="clearfix">
              <span class="sc-font">个人账单管理</span>
              <el-select v-model="type"  placeholder="请选择消费类型" style="width:100%;margin-top: 15px" clearable>
                <el-option
                  v-for="item in types"
                  :key="item.label"
                  :label="item.label"
                  :value="item.label">
                </el-option>
              </el-select>
              <el-date-picker
                style="margin-top: 10px;width:100%;"
                v-model="date"
                align="right"
                type="date"
                placeholder="选择日期"
                value-format="yyyy-MM-dd">
              </el-date-picker>
              <el-input v-model="desc" placeholder="请输入消费描述" style=" margin-top: 10px;"></el-input>
              <el-input v-model="money" placeholder="请输入消费金额" style=" margin-top: 10px;" oninput="value=value.replace(/^\.+|[^\d.]/g,'')" @blur="salaryChange"></el-input>
              <el-row   style="margin-top: 10px;" :gutter="20">
                <el-col :span="6">
                  <el-button @click="restForm" :loading="submitloading">重 置</el-button>
                </el-col>
                <el-col :span="6">
                  <el-button type="primary" @click="queryData" :loading="submitloading">查 询</el-button>
                </el-col>
              </el-row>
            </div>
          </el-card>
          <div class="bk-foot">
            <div v-for="item in result">
              <el-card shadow="hover">
                <div class="desc-main">
                  <el-row justify="space-between">
                    <el-col :span="18">
                      <div class="desc-desc">
                        {{item.desc}}
                      </div>
                      <div class="desc-type">
                        <el-tag size="mini" effect="plain">
                          {{item.type}}
                        </el-tag>
                      </div>
                      <div class="desc-date">
                        {{item.date}}
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="desc-dele">
                        <i class="el-icon-close" @click="deleteData(item)"></i>
                      </div>
                      <div class="desc-money" @click="openEditData(item)">
                        <i class="desc-money-icon">¥</i> {{item.money}}
                      </div>
                    </el-col>
                  </el-row>
                </div>
              </el-card>
            </div>
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
      title="请输入修改金额"
      :visible.sync="editForm.editdialog"
      width="90%"
      :before-close="closeEditData">
      <a>ID: {{editForm.editID}}</a><br>
      <a>类型: {{editForm.editType}}</a><br>
      <a>描述: {{editForm.editDesc}}</a><br>
      <a>日期: {{editForm.editDate}}</a><br>
      <el-input v-model="editForm.editmoney" placeholder="请输入消费金额" style=" margin-top: 10px;" oninput="value=value.replace(/^\.+|[^\d.]/g,'')" @blur="salaryChange"></el-input>
      <br>
      <span slot="footer" class="dialog-footer">
    <el-button @click="closeEditData">取 消</el-button>
    <el-button type="primary" @click="editData">确 定</el-button>
  </span>
    </el-dialog>
  </div>
</template>
<script>
const qs = require('qs') //引入序列化功能
import {FB_TYPE} from './fb'
export default {
  name: 'fbmanager',
  components: {},
  props: {},
  data() {
    return {
      IP:'http://127.0.0.1:9988',
      loginDialogVisible:false,
      result:[],
      form: {
        username:'',
        pwd:''
      },
      type:'',// 类型
      userid:'',// 当前用户
      money:'',//金额
      desc:'',// 描述
      date:'',// 时间
      deleteID: '',// 删除id
      submitloading:false,//提交加载控制
      editForm:{
        editDesc:'',
        editDate:'',
        editType:'',
        editID:'', // 修改id
        editmoney:'',// 编辑 金额
        editdialog:false,// 修改
      },
      types:[],
    }
  },
  computed: {},
  watch: {
  },
  created() {
    this.userid = localStorage.getItem('userid')
    this.types = FB_TYPE
    this.loading()
  },
  mounted() {
  },
  methods: {
    loading(){
      if(this.online()){
        this.desc = ''
        this.money = ''
        this.date = ''
        this.type = ''
        this.queryData()
      }else{
        this.outline()
      }
    },
    queryData(){
      if(this.online()){
        this.$request.get(this.IP + '/ylmanager/list' + '?userid=' + this.userid + '&type=' + this.type + '&descs=' + this.desc + '&money=' + this.money + '&date=' + this.date)
          .then((res) => {
            if(res.data.code === 200){
             // this.$message({
             //   duration: 1500,
             //   showClose: true,
             //   message: '查询成功',
             //   type:'success'
             // });
              this.result = res.data.data
            }else{
              this.result = []
            }
          })
      }else{
        this.outline()
      }
    },
    deleteData(item){
      console.log(item)
      if(this.online()){
        if(item.id){
          this.$confirm('请确认删除该账单?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.$request.get(this.IP + '/ylmanager/delete' + '?userid=' + this.userid + '&id=' + item.id)
              .then((res) => {
                if(res.data.code === 200){
                  this.$message({
                    duration: 1500,
                    showClose: true,
                    message: '删除成功',
                    type:'success'
                  });
                  this.loading()
                }else{
                  this.$message({
                    duration: 1500,
                    showClose: true,
                    message: '删除遇到异常',
                    type:'error'
                  });
                  this.loading()
                }
              })
          }).catch(() => {
            this.$message({
              duration: 1500,
              showClose: true,
              type: 'info',
              message: '已取消删除'
            });
          });
          // TODO 调用删除接口
        }else{
          alert("当前删除的信息无效！！")
        }
      }else{
        this.outline()
      }
    },
    editData(){
      if(this.editForm.editmoney && this.editForm.editID){
        this.$request.get(this.IP + '/ylmanager/edit' + '?userid=' + this.userid + '&money=' + this.editForm.editmoney + '&id=' + this.editForm.editID)
          .then((res) => {
            if(res.data.code === 200){
              this.$message({
                duration: 1500,
                showClose: true,
                message: '修改成功',
                type:'success'
              });
              this.closeEditData()
              this.loading()
            }else{
              this.$message({
                duration: 1500,
                showClose: true,
                message: '修改遇到异常',
                type:'error'
              });
              this.loading()
            }
          })
      }else{
        alert("当前修改无效！")
      }
    },
    openEditData(item){
      console.log(item)
      this.editForm.editID = item.id
      this.editForm.editType = item.type
      this.editForm.editDesc = item.desc
      this.editForm.editDate = item.date
      this.editForm.editdialog = true
    },
    closeEditData(){
      this.editForm.editdialog = false
      this.editForm.editID = ''
      this.editForm.editType = ''
      this.editForm.editDesc = ''
      this.editForm.editDate = ''
      this.editForm.editmoney = ''
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
              console.log(this.userid)
              this.loading()
              this.loginDialogVisible = false
              this.$message({
                duration: 1500,
                showClose: true,
                message: '登录成功',
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

    clear(){
      this.userid = ''
    },
    salaryChange(e){
      this.money = e.target.value
    },
    restForm(){
      this.submitloading = true
      this.type = ''
      this.money = ''
      this.desc = ''
      this.date = ''
      this.submitloading = false
      this.loading()
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
      this.$message({
        message: '请先登录',
        duration: 1500,
        showClose: true,
        type: 'info'
      });
    },
    tobk(){
      this.$router.push('/')
    },
    tosc(){
      this.$router.push('/sc')
    },
  }
}
</script>
<style lang="css" scoped>
.desc-main{

}
.desc-date{
  position: relative;
  bottom: -10px;
  color: #cacaca;
}
.desc-dele{
  color: #cacaca;
  position: relative;
  right: -70px;
  top: -10px;
}
.desc-money{
  position: relative;
  top: 5px;
  font-size: 30px;
  font-weight: bold;
  color: #f15728;
  right: 5px;
}
.desc-money-icon{
  font-size: 25px;
  margin-right: -5px;
}
.desc-type{
  position: relative;
  margin-top: 10px;
}
.desc-desc{
  position: relative;
  font-size: 30px;
  font-weight: bold;
  /*margin-top: -10px;*/

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
  background-color: #ce6d85;
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
.el-card{
  margin-top: 5px;
}
</style>
