<template>
  <div id="trend-chart">
    <div class="chartarea" align="center">
      <h1>TrendChart - Monthly Average Rating</h1>
      <div id="chart"/>
      <v-chart :options="sampleChart" />
    </div>
    <Divider/>
  </div>
</template>

<script>
import axios from 'axios'
import ECharts from 'vue-echarts'
import 'echarts/lib/chart/line'
import 'echarts/lib/component/legend'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/toolbox'

export default {
  name: 'TrendChart',
  components: {
    'v-chart': ECharts
  },
  data() {
    return {
      modelIDs: [],
      models: [],
      reviewData: [],
      sampleChart: {}
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
  methods: {
    getReviewData() {
      axios.post('http://127.0.0.1:8080/api/v1/ratings/', {'models': this.models})
        .then(response => {
          let chartInfo = {
            color: ['#FC3535', '#FC8935', '#9B983B', '#6BC227', '#27C255', '#27C2B3',
              '#2779C2', '#3030B6', '#7630B6', '#A64495', '#481528', '#000000'
            ],
            tooltip: {
              trigger: 'item',
              formatter: "{a} <br/>{b}'s Average : {c}"
            },
            legend: {
              bottom: 10,
              data: this.models,
            },
            toolbox: {
              feature: {
                saveAsImage: {
                  type: 'jpeg',
                  name: 'review_average_rating'
                }
              }
            },
            xAxis: [{
              type: 'category',
              axisLine: {
                lineStyle: {
                  color: '#000000'
                }
              },
              data: ['2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06',
                '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12',
                '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06',
                '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12'
              ]
            }, ],
            backgroundColor : "white",
            yAxis: [{
              type: 'value',
              name: 'Average Rating'
            }],
            series: []
          }
          this.reviewData = response.data
          for (let i = 0; i < this.models.length; i++) {
            const filterModelID = this.models[i]
            const monthlyReviewData = this.reviewData[filterModelID]
            let ratingAvg = []
            for (let j = 18; j < 20; j++) {
              for (let k = 1; k < 10; k++) {
                let averageValue = monthlyReviewData['20' + j.toString() + '-0' + k.toString()][0].average
                if (averageValue === null) {
                  ratingAvg.push(0)
                } else {
                  ratingAvg.push(parseFloat(averageValue.toFixed(2)))
                }
              }
              for (let k = 10; k < 13; k++) {
                let averageValue = monthlyReviewData['20' + j.toString() + '-' + k.toString()][0].average
                if (averageValue === null) {
                  ratingAvg.push(0)
                } else {
                  ratingAvg.push(parseFloat(averageValue.toFixed(2)))
                }
              }
            }
            var seriesInfo = {
              name: filterModelID,
              type: 'line',
              data: ratingAvg
            }
            chartInfo.series.push(seriesInfo)
          }
          this.sampleChart = chartInfo
        })
    }
  },
  watch: {
    models: {
      handler() {
        this.getReviewData()
      }
    }
  }
}
</script>

<style>
#trend-chart {
  padding-top : 10px;
  text-align : center;
}

.chartarea{
  background: white;
  margin: 10px;
  border-radius: 10px;
  padding-top : 10px;
}
</style>