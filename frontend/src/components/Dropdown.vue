<template>
    <span>
        <span>
            <p class="selectorline">Brand Select</p>
            <Select v-model="brands" multiple style="width : 300px" class="selector" :max-tag-count="3">
                <Option v-for="item in brandList" :value="item.value" :key="item.value">{{ item.label }}</Option>
            </Select>
        </span>
        <span style="margin-left: 50px;">
            <p class="selectorline">Model Select</p>
            <Select v-model="models" multiple :max-tag-count="2" style="width : 400px;" class="selector">
                <Option v-for="item in modelList" :value="item.value" :key="item.value">{{ item.label }}</Option>
            </Select>
        </span>
    </span>
</template>

<script>
    import Vue from 'vue'
    import axios from 'axios'

    Vue.prototype.$EventBus = new Vue()
    export default {
        data() {
            return {
                modelList: [],
                brandList: [],
                models: [],
                brands: []
            }
        },
        methods: {
            getBrands() {
                axios.get('http://127.0.0.1:8080/api/v1/brands/')
                    .then(response => {
                        for (let i in response.data) {
                            let data = {
                                "label": response.data[i].key,
                                "value": response.data[i].key
                            }
                            this.brandList.push(data)
                        }
                    })
            },
            getModels() {
                axios.get('http://127.0.0.1:8080/api/v1/models/')
                    .then(response => {
                        for (let i in response.data) {
                            let obj = {}
                            obj["label"] = response.data[i]["key"]
                            obj["value"] = response.data[i]["key"]
                            this.modelList.push(obj)
                        }
                    })
            }
        },
        mounted() {
            this.getBrands()
            this.getModels()
            this.$EventBus.$emit("modelList", this.modelList)
        },
        watch: {
            models(newValue) {
                this.$EventBus.$emit("models", newValue)
            },
            brands(newValue) {
                this.$EventBus.$emit("brands", newValue)
                this.modelList = []
                this.models = []

                axios
                    .post('http://127.0.0.1:8080/api/v1/brandmodel/', {
                        'brands': this.brands
                    })
                    .then(response => {
                        for (let i in response.data) {
                            let model = response.data[i]['_source'].model_id
                            let data = {
                                "label": model,
                                "value": model
                            }
                            this.modelList.push(data)
                        }
                    })
            }
        },
    }
</script>

<style>
    .selectorline {
        color: white;
        display: inline;
        margin-right: 5px;
    }

    .selector {
        margin: 3px;
    }
</style>