<template>
    <div class="home">
        <div class="container mt-2">
            <div v-for="family in families"
                 :key="family.pk">
                <p class="mb-0">Family name:
                    <span class="question-author">{{ family.name }}</span>
                </p>
                <hr>
            </div>
            <div class="my-4">
                <p v-show="loadingQuestions">...loading...</p>
                <button
                        v-show="next"
                        @click="getQuestions"
                        class="btn btn-sm btn-outline-success"
                >Load More
                </button>
            </div>
        </div>
    </div>
</template>

<script>
  import {apiService} from "@/common/api.service.js";

  export default {
    name: "home",
    data() {
      return {
        families: [],
        next: null,
        loadingQuestions: false
      }
    },
    methods: {
      getQuestions() {
        // make a GET Request to the questions list endpoint and populate the questions array
        let endpoint = "/api/families/";
        if (this.next) {
          endpoint = this.next;
        }
        this.loadingQuestions = true;
        apiService(endpoint)
          .then(data => {
            this.families.push(...data.results)
            this.loadingQuestions = false;
            if (data.next) {
              this.next = data.next;
            } else {
              this.next = null;
            }
          })
      }
    },
    created() {
      this.getQuestions()
      document.title = "Families List";
    }
  };
</script>

<style scoped>
    .question-author {
        font-weight: bold;
        color: #DC3545;
    }

    .question-link {
        font-weight: bold;
        color: black;
    }

    .question-link:hover {
        color: #343A40;
        text-decoration: none;
    }
</style>
