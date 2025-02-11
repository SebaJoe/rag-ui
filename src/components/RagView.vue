<template>

  <div class="container-fluid">
    <nav class="navbar fixed-bottom" id="bottom-bar">
      <div class="mx-auto" id="chatif">
        <div class="container">
          <div class="row">
            <div class="col"> 
              <textarea id="chatbox" placeholder="Write your queries here..."></textarea>
            </div>
          </div>
          <div class="row">
            <div class="col">
              <div class="btn-group">
                <button class="btn btn-light">
                        Option 1
                </button>
                <button class="btn btn-light">
                        Option 2
                </button>
                <button class="btn btn-light">
                        Option 3
                </button>
              </div>
            </div>
            <div class="col-1">
              <button type="button" id="enter-button" class="btn btn-dark">
                <i class="bi bi-arrow-return-right"></i>
              </button>
            </div>
          </div>
        </div>
      </div>  
    </nav>
  </div>

</template>


<script>

  import CodeOut from './CodeOut.vue';

  export default {
    components: {
        CodeOut,
    },
    data () {

    },
    methods: {

    }
  }

</script>


<style>

#bottom-bar {
  height: 30%;
}

#chatif {
  border-top: #E5E4E2 solid 0.5px;
  width: 40%;
}

#chatbox {
    border: none;
    overflow: auto;
    outline: none;

    padding-top: 15px;

    -webkit-box-shadow: none;
    -moz-box-shadow: none;
    box-shadow: none;

    resize: none; /*remove the resize handle on the bottom right*/

    height: 150px;

    width: 40%;
}

#enter-button {

  height: 36px;
  width: 50px;
  border-radius: 20px;
}

</style>