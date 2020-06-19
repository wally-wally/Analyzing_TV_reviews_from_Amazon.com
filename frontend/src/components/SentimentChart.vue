<template>
  <div id="sentiment-chart">
    <div class="chartarea" align="center">
      <h1>Bar Chart - Sentiment Analysis</h1>
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
  name: 'TrendChart',
  components: {
    'v-chart': ECharts
  },
  data() {
    let colors = ['#2779C2', '#FC3535']
    return {
      modelIDs: [],
      models: [],
      reviewData: [],
      seriesData: [],
      sampleChart: {
        color: colors,
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          bottom: 10,
          data: this.models,
        },
        toolbox: {
          feature: {
            saveAsImage: {
              type: 'jpeg',
              name: 'review_sentiment'
            }
          }
        },
        dataset: {
          source: [
            ['product', 'Positive', 'Negative']
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
          {type: 'bar'}, {type: 'bar'}
        ]
      }
    }
  },
  mounted() {
    this.$EventBus.$on("models", value => {
      this.models = value
    })
    this.$EventBus.$on("modelList", value => {
      this.modelIDs = value
    })
  },
  watch: {
    models: {
      handler() {
        axios.post('http://127.0.0.1:8080/api/v1/sentiments/', {'models': this.models})
          .then(response => {
            this.sampleChart.dataset.source = []
            let sourceArray = this.sampleChart.dataset.source
            sourceArray.push(['product', 'Positive', 'Negative'])
            for (let i = 0; i < response.data.length; i++) {
              const filterModelID = this.models[i]
              const reviewSentiInfo = response.data[i][filterModelID]
              sourceArray.push([filterModelID, reviewSentiInfo[0], reviewSentiInfo[1]])
            }
            this.sampleChart.dataset.source = sourceArray
          })
      }
    }
  }
}
</script>

<style>
#sentiment-chart {
  text-align : center;
}

.chartarea{
  background: white;
  border-radius: 10px;
  padding-top : 10px;
}
</style>