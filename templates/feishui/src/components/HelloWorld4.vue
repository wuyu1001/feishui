<template>
  <div class="hello">
    <el-row>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item>数据上传</el-breadcrumb-item>
      </el-breadcrumb>
    </el-row>
    <el-row>
      <el-collapse>
        <el-collapse-item title="搜索" name="1">
          <el-row class="searchBox elrow">
            <div v-for="(v, i) in student.columns" :key="i">
              <span class="label">{{ v.title }}</span>
              <el-input placeholder="请输入内容" v-model="v.search_value">
              </el-input>
            </div>
          </el-row>
          <el-row>
            <el-button type="success" @click="search()">搜索</el-button>
            <el-button type="success" @click="reset()">重置</el-button>
          </el-row>
        </el-collapse-item>
      </el-collapse>
    </el-row>
    <el-row>
      <el-button type="success" @click="create_upload_data()"
        >重新生成待上传数据
      </el-button>
      <el-button type="success" @click="beginUpload()"
        >开始上传待上传数据</el-button
      >
    </el-row>
    <el-row class="elrow">
      <el-col :span="24"
        ><div class="grid-content bg-purple"></div>
        <el-table :data="student.table_zzjg_xsxx" border style="width: 100%">
          <el-table-column type="index"></el-table-column>
          <el-table-column
            v-for="(v, i) in student.columns"
            :prop="v.field"
            :label="v.title"
            :width="v.width"
            :key="i"
          >
            <template slot-scope="scope">
              <div>
                <span v-show="scope.row.is_edit == 1 && v.field != 'flsh'">
                  <el-input
                    size="mini"
                    placeholder="请输入内容"
                    v-model="scope.row[v.field]"
                  >
                  </el-input>
                </span>
                <span
                  v-show="
                    scope.row.is_edit == 0 ||
                    (scope.row.is_edit == 1 && v.field == 'flsh')
                  "
                  style="text-align: center"
                  >{{ scope.row[v.field] }}</span
                >
              </div>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          @size-change="handleSizeChange1"
          @current-change="handleCurrentChange1"
          :current-page="currentPage1"
          :page-sizes="[10, 20, 40, 80]"
          :page-size="size1"
          layout="total,sizes, prev, pager, next,jumper"
          :total="total1"
        >
        </el-pagination>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  props: {
    msg: String,
  },
  data() {
    return {
      dialogVisible: false,
      percentage: 0,
      socket: null,
      student: {
        columns: [
          { field: "flsh", title: "标识号", width: 250, search_value: "" },
          { field: "sjcz", title: "数据操作", width: 100, search_value: "" },
          { field: "xh", title: "学号", width: 100, search_value: "" },
          { field: "xm", title: "姓名", width: 100, search_value: "" },
          { field: "xb", title: "性别", width: 80, search_value: "" },
          { field: "csrq", title: "生日", width: 100, search_value: "" },
          { field: "csd", title: "出生地", width: 100, search_value: "" },
          { field: "jg", title: "籍贯", width: 100, search_value: "" },
          { field: "mzm", title: "民族", width: 80, search_value: "" },
          { field: "gjdq", title: "国籍地区", width: 100, search_value: "" },
          {
            field: "sfzjlxm",
            title: "证件类型码",
            width: 100,
            search_value: "",
          },
          {
            field: "sfzjlxmc",
            title: "证件类型名称",
            width: 100,
            search_value: "",
          },
          { field: "sfzjh", title: "证件号", width: 150, search_value: "" },
          { field: "xjzt", title: "学籍", width: 80, search_value: "" },
          { field: "xslbm", title: "学生类别码", width: 100, search_value: "" },
          { field: "xslbmc", title: "学生类别", width: 100, search_value: "" },
          { field: "szbh", title: "班号", width: 100, search_value: "" },
          { field: "sznj", title: "年级", width: 100, search_value: "" },
          { field: "yxsh", title: "院系", width: 100, search_value: "" },
          { field: "zyh", title: "专业", width: 100, search_value: "" },
          { field: "xz", title: "学制", width: 80, search_value: "" },
          { field: "frxnd", title: "入学年度", width: 100, search_value: "" },
          { field: "flxnd", title: "离校年度", width: 100, search_value: "" },
          { field: "xkml", title: "学科门类", width: 100, search_value: "" },
          { field: "xsdqzt", title: "当前状态", width: 100, search_value: "" },
          { field: "xqdm", title: "学区代码", width: 100, search_value: "" },
          { field: "qyzt", title: "启用状态", width: 100, search_value: "" },
          { field: "fzsbs", title: "住宿标识", width: 100, search_value: "" },
          { field: "bdtime", title: "报道时间", width: 100, search_value: "" },
          { field: "bz", title: "备注", width: 100, search_value: "" },
        ],
        table_zzjg_xsxx: [],
      },
      currentPage1: 1,
      size1: 10,
      total1: 0,
    };
  },
  methods: {
    getTableData(tablename, pagesize, page, search_value) {
      this.$axios
        .post(
          "http://127.0.0.1:5000/table/" +
            tablename +
            "/" +
            pagesize +
            "/" +
            page,
          { search_value: search_value }
        )
        .then((x) => {
          this.student.table_zzjg_xsxx = x.data.data;
          this.student.table_zzjg_xsxx.map((x) => {
            x.is_edit = false;
            return x;
          });
          this.total1 = x.data.total;
        });
    },
    handleSizeChange1(val) {
      this.size1 = val;
      this.getTableData("zzjg_xsxx_upload", val, this.currentPage1);
    },
    handleCurrentChange1(val) {
      this.getTableData("zzjg_xsxx_upload", this.size1, val);
    },
    pwdChange(row, index, is_save) {
      let obj = {
        ...row,
        is_edit: !row.is_edit,
      };
      this.$set(this.student.table_zzjg_xsxx, index, obj);
      if (is_save) {
        this.$axios
          .post(
            "http://127.0.0.1:5000/modifyTable/zzjg_xsxx_upload",
            this.student.table_zzjg_xsxx[index]
          )
          .then((x) => {
            this.$message(x.data);
            // console.log(x.data);
          });
        // console.log(this.student.table_zzjg_xsxx[index]);
      }
    },
    search() {
      let v_where = "where 1=1 ";
      this.student.columns.forEach((x) => {
        if (x.search_value != "") {
          v_where += ` and ${x.field} like '%${x.search_value}%'`;
        }
      });
      this.getTableData(
        "zzjg_xsxx_upload",
        this.size1,
        this.currentPage1,
        v_where
      );
    },
    reset() {
      this.student.columns.forEach((x) => {
        x.search_value = "";
      });
      this.getTableData(
        "zzjg_xsxx_upload",
        this.size1,
        this.currentPage1,
        undefined
      );
    },
    beginUpload() {
      this.$axios.post("http://127.0.0.1:5000/beginupload").then((x) => {
        this.$message(x.data);
      });
    },
    create_upload_data() {
      this.$axios.post("http://127.0.0.1:5000/create_upload_data").then((x) => {
        this.$message(x.data);
        this.getTableData("zzjg_xsxx_upload", this.size1, 1);
      });
    },
  },
  mounted() {
    this.getTableData("zzjg_xsxx_upload", this.size1, 1);
  },
};
</script>


<style scoped>
.el-input {
  width: auto;
}
/deep/ .searchBox .el-input__inner {
  text-align: center;
  width: 150px;
}
.searchBox {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.searchBox div {
  display: flex;
  align-items: center;
  margin-bottom: 2px;
}
.label {
  display: inline-block;
  width: 75px;
  font-weight: bold;
  text-align: justify;
  text-align-last: justify;
  font-size: 8px;
  /* color: #909399; */
  padding: 13px;
}
</style>
