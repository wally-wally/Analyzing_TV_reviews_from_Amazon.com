<template>
    <div id="reviewtrend-chart">
    <div class="chartarea" align="center">
      <h1>Review Total Count Chart</h1>
      <v-chart :options="sampleChart" />
    </div>
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
  name: 'TotalReviewChart',
  components: {
    'v-chart': ECharts
  },
  data() {
    return {
      modelIDs: ['B07NC9SPBF', 'B07F26ZQ8L', 'B07JK98NNQ', 'B01A0LGS3Q', 'B07N4MVTXB', 'B01LXHXGZX',
        'B01N5KGXUX', 'B073JP6WK4', 'B0755M5VCQ', 'B07M8D8JDK', 'B07NHQ4CXM', 'B07FPQXN46'
      ],
      models: [],
      reviewData: [],
      sampleChart: {}
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
        axios.post('http://127.0.0.1:8080/api/v1/ratings/', {'models': this.models})
          .then(response => {
            let chartInfo = {
              color: ['#FC3535', '#FC8935', '#9B983B', '#6BC227', '#27C255', '#27C2B3',
                '#2779C2', '#3030B6', '#7630B6', '#A64495', '#481528', '#000000'
              ],
              tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}'s Count : {c}"
              },
              legend: {
                bottom: 10,
                data: this.models,
              },
              toolbox: {
                feature: {
                  saveAsImage: {
                    type: 'jpeg',
                    name: 'review_total_count'
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
              yAxis: [{
                type: 'value',
                name: 'Total Review Count'
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
                  let reviewCntValue = monthlyReviewData['20' + j.toString() + '-0' + k.toString()][0]['review_count']
                  if (reviewCntValue === null || reviewCntValue === 1e-7) {
                    ratingAvg.push(0)
                  } else {
                    ratingAvg.push(parseFloat(reviewCntValue.toFixed(2)))
                  }
                }
                for (let k = 10; k < 13; k++) {
                  let reviewCntValue = monthlyReviewData['20' + j.toString() + '-' + k.toString()][0]['review_count']
                  if (reviewCntValue === null || reviewCntValue === 1e-7) {
                    ratingAvg.push(0)
                  } else {
                    ratingAvg.push(parseFloat(reviewCntValue.toFixed(2)))
                  }
                }
              }
              let seriesInfo = {
                name: filterModelID,
                type: 'line',
                data: ratingAvg
              }
              chartInfo.series.push(seriesInfo)
            }
            this.sampleChart = chartInfo
          })
      }
    }
  }
}
</script>

<style>
#reviewtrend-chart {
  text-align : center;
}

.chartarea{
  background:white;
  border-radius: 10px;
  padding-top : 10px;
  height: 550px;
}
</style>