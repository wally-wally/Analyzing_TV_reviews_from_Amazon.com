<template>
    <div>
        <div class="scroll">
            <template v-for='review in reviews' >
                <div :key="review.review_id" class="review" @click="reviewselect(review)">
                    <Card :bordered="false">
                        <a @click="reviewselect(review)" class="review-title review-card" slot="title">
                            <h3>{{review.title}}</h3>
                        </a>
                        <span class="review-content review-card" slot="title">{{review.content}}</span>
                        <p class="review-info review-card">
                            {{review.model_id}} | {{review.date}} | 
                            <Rate allow-half disabled v-model="review.rating" />
                        </p>
                    </Card>
                </div>
            </template>
        </div>

        <Modal
            v-model="modal"
            :title="select_review.title">
            <p>{{select_review.content}}</p>
        </Modal>

        <div class="pagination">
            <Page :total="review_cnt" @on-change="changePage"/>
        </div>
    </div>
</template>

<script >
import axios from 'axios'
    
export default {
    name : 'reviewList',
    data(){
        return {
            reviews : [],
            review_cnt : 0,
            models : [],
            select_review : {},
            modal : false
        }
    },
    mounted () {
        this.$EventBus.$on("models", value => {
            this.models = value
        })
    },
    methods: {
        changePage(pageNumber) {
            let from = (pageNumber-1)*10
            this.getReviewList(from)
        },
        reviewselect(selected){
            this.select_review = selected
            this.modal = true
        },
        getReviewList(from){
            let requestData = {
                "models" : this.models,
                "frompage" : from
            }
            
            axios.post('http://127.0.0.1:8080/api/v1/reviews/', requestData)
                .then(response => {
                    this.reviews = []
                    for(let i in response.data['hits']){
                        this.reviews.push(response.data['hits'][i]['_source'])
                    }
                    this.review_cnt = response.data['total']['value']
                })
        }
    },
    watch: {
        models(newValue, oldValue) {
            this.getReviewList(0)
        }
    },
}
</script>

<style>
body {
    overflow: hidden;
}

.review {
    background:#eee;
    margin: 10px;
    border-radius: 10px;
}

.review-card {
    text-align: left;
}

.review-content {
    font-size : 17px;
    margin : 20px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
}

.pagination {
    margin-top : 20px;
    text-align : center;
}

.scroll {
    max-height: 600px;
    overflow-y: scroll;
}
</style>