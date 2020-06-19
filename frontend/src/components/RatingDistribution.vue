<template>
  <div id="distribution-chart">
    <div class="chartarea" align="center">
      <h1>Model's Rating Distribution</h1>
      <v-chart :options="sampleChart" />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ECharts from 'vue-echarts'
import 'echarts/lib/chart/bar'
import 'echarts/lib/component/legend'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/toolbox'
import 'echarts/lib/component/axisPointer'

export default {
  name: 'RatingDistribution',
  components: {
    'v-chart': ECharts
  },
  data() {
    let colors = ['#1E3BF8', '#67EB45', '#DBE01D', '#FAB443', '#FB4D2E']
    return {
      models: [],
      sampleChart: {
        color: colors,
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        backgroundColor: '#FFFFFF',
        legend: {
          bottom: 10,
          data: this.models,
        },
        toolbox: {
          feature: {
            saveAsImage: {
              type: 'jpeg',
              name: 'review_trend'
            }
          }
        },
        dataset: {
          source: [
            ['product', '5points', '4points', '3points', '2points', '1point']
          ]
        },
        xAxis: {
          type: 'category'
        },
        yAxis: {
          type: 'value',
          name: "Review's Count"
        },
        series: [
          {type: 'bar'}, {type: 'bar'}, {type: 'bar'}, {type: 'bar'}, {type: 'bar'}
        ]
      }
    }
  },
  mounted() {
    this.$EventBus.$on("models", value => {
      this.models = value
    })
  },
  watch: {
    models: {
      handler() {
        axios.post('http://127.0.0.1:8080/api/v1/num_rating/', {'models': this.models})
          .then(response => {
            this.sampleChart.dataset.source = []
            let sourceArray = []
            sourceArray.push(['product', '5points', '4points', '3points', '2points', '1point'])
            for (let i = 0; i < this.models.length; i++) {
              let chartData = []
              const filterModelID = this.models[i]
              chartData.push(filterModelID)
              for (let j = 4; j > -1; j--) {
                chartData.push(response.data[filterModelID][j])
              }
              sourceArray.push(chartData)
            }
            this.sampleChart.dataset.source = sourceArray
          })
      }
    }
  }
}
</script>

<style>
#distribution-chart {
  text-align : center;
}

.chartarea{
  background: white;
  border-radius: 10px;
  padding-top : 10px;
}
</style>