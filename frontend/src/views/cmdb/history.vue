<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        placeholder="请输入内容"
        clearable
        prefix-icon="el-icon-search"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter"
        @clear="handleFilter"
      />
      <el-button
        class="filter-item"
        type="primary"
        icon="el-icon-search"
        @click="handleFilter"
      >{{ "搜索" }}</el-button>
    </div>

    <el-table
      :data="list"
      v-loading="listLoading"
      border
      style="width: 100%"
      @sort-change="handleSortChange"
    >
      <el-table-column label="命令" prop="cmd"></el-table-column>
      <el-table-column label="使用次数" prop="num"></el-table-column>
      <el-table-column label="创建时间" prop="create_time"></el-table-column>
      <el-table-column label="上次使用时间" prop="update_time"></el-table-column>
    </el-table>
    <div class="table-pagination">
      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="listQuery.offset"
        :limit.sync="listQuery.limit"
        @pagination="getList"
      />
    </div>
  </div>
</template>

<script>
import { history } from "@/api/all";
import Pagination from "@/components/Pagination";

export default {
  name: "history",

  components: { Pagination },
  data() {
    return {
      list: [],
      total: 0,
      listLoading: true,
      loading: true,
      listQuery: {
        offset: 1,
        limit: 20,
        search: undefined,
        ordering: undefined
      }
    };
  },
  computed: {},
  created() {
    this.getList();
  },
  methods: {
    getList() {
      this.listLoading = true;
      history.requestGet(this.listQuery).then(response => {
        this.list = response.results;
        this.total = response.count;
        this.listLoading = false;
      });
    },
    handleFilter() {
      this.getList();
    },
    handleSortChange(val) {
      if (val.order === "ascending") {
        this.listQuery.ordering = val.prop;
      } else if (val.order === "descending") {
        this.listQuery.ordering = "-" + val.prop;
      } else {
        this.listQuery.ordering = "";
      }
      this.getList();
    }
  }
};
</script>
