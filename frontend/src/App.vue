<template>
  <div id="app" class='layout'>
    <Layout>
      <div class="header" style="z-index:2">
        <span class="dropdown"><Dropdown/></span>
        <span class="title">  <Icon type="ios-stats-outline" size="50" style="margin-right:10px"/>Analytics TV Review</span>
      </div>
      <Row class="content">
        <Col span="12">
          <ReviewList/>
        </Col>
        <Col span="12">
          <Row span="6">
            <RadioGroup v-model="selectChart" type="button" class="radiobutton" align="center">
              <Radio label="Total_Review"></Radio>
              <Radio label="Average_Rating"></Radio>
              <Radio label="Sentiment_Analysis"></Radio>
              <Radio label="Rating_Distribution"></Radio>
            </RadioGroup>
          </Row>
          <Row span="18">
            <TrendChart v-show="selectChart == 'Average_Rating'"/>
            <SentimentChart v-show="selectChart == 'Sentiment_Analysis'"/>
            <ReviewTrendChart v-show="selectChart == 'Total_Review'"/>
            <RatingDistribution v-show="selectChart == 'Rating_Distribution'"/>
          </Row>
        </Col>
      </Row>
    </Layout>
  </div>
</template>

<script>
import ReviewList from './components/ReviewList.vue'
import Dropdown from './components/Dropdown.vue'
import TrendChart from './components/TrendChart.vue'
import SentimentChart from './components/SentimentChart.vue'
import ReviewTrendChart from './components/ReviewTrendChart.vue'
import RatingDistribution from './components/RatingDistribution.vue'

export default {
  name: 'app',
  components: {
    ReviewList,
    Dropdown,
    TrendChart,
    SentimentChart,
    ReviewTrendChart,
    RatingDistribution
  },
  data(){
    return {
      selectChart : "Total_Review"
    }
  }
}
</script>

<style>
html {
  overflow-y: hidden;
}

.header {
  padding : 20px;
  height : 80px;
  background-image: linear-gradient(#8e8b8b, #5f5f5f);
}

.title {
  float: right;
  font-size: 25px;
  font-weight : bold;
  margin-right : 20px;
  color : white;
}

.radiobutton {
  float : right;
  margin: 10px 20px 0 0;
}
</style>
