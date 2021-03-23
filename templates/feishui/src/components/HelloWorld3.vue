<template>
  <div>
    <el-row>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item>差异数据</el-breadcrumb-item>
      </el-breadcrumb>
    </el-row>
    <el-tabs type="border-card">
      <el-tab-pane label="新增数据">
        <!-- <el-button type="primary" @click.native="compare()">重新对比</el-button> -->

        <el-row class="elrow">
          <el-col :span="24"
            ><div class="grid-content bg-purple"></div>
            <el-table :data="table_zzjg_xsxx_new" border style="width: 100%">
              <el-table-column prop="flsh" label="标识号" width="250">
              </el-table-column>
              <el-table-column prop="xh" label="学号" width="100">
              </el-table-column>
              <el-table-column prop="xm" label="姓名" width="100">
              </el-table-column>
              <el-table-column prop="xb" label="性别" width="50">
              </el-table-column>
              <el-table-column prop="csrq" label="生日" width="100">
              </el-table-column>
              <el-table-column prop="mzm" label="民族" width="50">
              </el-table-column>
              <el-table-column prop="sfzjh" label="身份证件号" width="180">
              </el-table-column>
              <el-table-column prop="xjzt" label="学籍" width="50">
              </el-table-column>
              <el-table-column prop="xslbm" label="学生类别码" width="80">
              </el-table-column>
              <el-table-column prop="xslbmc" label="学生类别名称" width="80">
              </el-table-column>
              <el-table-column prop="szbh" label="班号" width="120">
              </el-table-column>
              <el-table-column prop="sznj" label="年级" width="80">
              </el-table-column>
              <el-table-column prop="yxsh" label="院系" width="80">
              </el-table-column>
              <el-table-column prop="zyh" label="专业" width="80">
              </el-table-column>
              <el-table-column prop="xz" label="学制" width="80">
              </el-table-column>
              <el-table-column prop="frxnd" label="入学年度" width="80">
              </el-table-column>
              <el-table-column prop="flxnd" label="离校年度" width="80">
              </el-table-column>
              <el-table-column prop="xsdqzt" label="当前状态" width="80">
              </el-table-column>
              <el-table-column prop="qyzt" label="启用状态" width="80">
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
      </el-tab-pane>
      <el-tab-pane label="变动数据">
        <el-row class="elrow">
          <el-col :span="24"
            ><div class="grid-content bg-purple"></div>
            <el-table :data="table_zzjg_xsxx_change" border style="width: 100%">
              <el-table-column prop="flsh" label="标识号" width="250">
              </el-table-column>

              <el-table-column
                v-for="(v, i) in student.columns.filter(
                  (x) => x.field !== 'flsh'
                )"
                :prop="v.field"
                :label="v.title"
                :width="v.width"
                :key="i"
                align="center"
              >
                <el-table-column label="新" width="100" align="center">
                  <template slot-scope="scope">
                    <span
                      :class="{
                        red:
                          scope.row[v.field + '_df1'] !==
                          scope.row[v.field + '_df2'],
                      }"
                      >{{ scope.row[v.field + "_df1"] }}</span
                    >
                  </template>
                </el-table-column>
                <el-table-column label="旧" width="100" align="center">
                  <template slot-scope="scope">
                    <span
                      :class="{
                        red:
                          scope.row[v.field + '_df1'] !==
                          scope.row[v.field + '_df2'],
                      }"
                      >{{ scope.row[v.field + "_df2"] }}</span
                    >
                  </template>
                </el-table-column>
              </el-table-column>
            </el-table>
            <el-pagination
              @size-change="handleSizeChange2"
              @current-change="handleCurrentChange2"
              :current-page="currentPage2"
              :page-sizes="[10, 20, 40, 80]"
              :page-size="size2"
              layout="total,sizes, prev, pager, next,jumper"
              :total="total2"
            >
            </el-pagination>
          </el-col>
        </el-row>
      </el-tab-pane>
    </el-tabs>
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
      table_zzjg_xsxx_new: [],
      table_zzjg_xsxx_change: [],
      currentPage1: 1,
      size1: 10,
      total1: 0,
      currentPage2: 1,
      size2: 10,
      total2: 0,

      student: {
        columns: [
          { field: "flsh", title: "标识号", width: 250, search_value: "" },
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
    };
  },
  methods: {
    compare(dataType, pagesize, page) {
      if (dataType === undefined) {
        this.$axios
          .get(
            "http://127.0.0.1:5000/compare/new" + "/" + pagesize + "/" + page
          )
          .then((x) => {
            // console.log(x);
            this.table_zzjg_xsxx_new = x.data.data;
            this.total1 = x.data.total;
          });
        this.$axios
          .get(
            "http://127.0.0.1:5000/compare/change" + "/" + pagesize + "/" + page
          )
          .then((x) => {
            // console.log(x);
            this.table_zzjg_xsxx_change = x.data.data;
            this.total2 = x.data.total;
          });
      } else {
        this.$axios
          .get(
            "http://127.0.0.1:5000/compare/" +
              dataType +
              "/" +
              pagesize +
              "/" +
              page
          )
          .then((x) => {
            // console.log(x);
            switch (dataType) {
              case "new":
                this.table_zzjg_xsxx_new = x.data.data;
                this.total1 = x.data.total;
                break;
              case "change":
                this.table_zzjg_xsxx_change = x.data.data;
                this.total2 = x.data.total;
                break;
              default:
                break;
            }
          });
      }
    },
    handleSizeChange1(val) {
      this.size1 = val;
      this.compare("new", val, this.currentPage1);
    },
    handleCurrentChange1(val) {
      this.compare("new", this.size1, val);
    },
    handleSizeChange2(val) {
      this.size2 = val;
      this.compare("change", val, this.currentPage2);
    },
    handleCurrentChange2(val) {
      this.compare("change", this.size2, val);
    },
  },
  mounted() {
    this.compare(undefined, this.size1, 1);
  },
};
</script>
<style scoped>
.red {
  display: inline-block;
  width: 100%;
  color: red;
  background: #f3f6f9;
}
</style>
