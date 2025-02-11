<template>
  <nav class="navbar sticky-top" style="background-color: white; padding: 0px">
    <div class="mx-auto" id="navtop">
      <div class="container">
        <div class="row flex justify-content-center">
          <div class="col-3">

          </div>
          <div class="col-3 logo-style text-center">
            <img src="../assets/Cosmic-AI.jpg" height="50px">
          </div>
          <div class="col-3 text-center dropdown">
            <h5 class="pad-dropdown">
              Export
            </h5>
            <div class="dropdown-content">
              <div class="container">
                <div class="row drop-row">
                  <div class="col drop-row">
                    Export to Jupyter Notebook
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
  <div class="container-fluid">
    <div class="mx-auto" id="chatcol">
      <div class="container">
        <div class="row">
          <div class="col">
            <div class="row">
              <div class="col">
                <MarkOut />
              </div>
            </div>
            <div class="row">
              <div class="col">
                <CodeOut />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <nav class="navbar fixed-bottom" id="bottom-bar" style="background-color: white;">
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
  import MarkOut from './MarkOut.vue';

  export default {
    components: {
        CodeOut,
        MarkOut,
    },
    data () {

    },
    methods: {

    }
  }

</script>


<style>

#bottom-bar {
  height: 250px;
}

#chatif {
  border-top: #E5E4E2 solid 0.5px;
  width: 50%;
  padding-bottom: 150px;
}

#navtop {
  border-bottom: #E5E4E2 solid 0.5px;
  width: 100%;
}

#chatcol {
  width: 50%;
  padding-bottom: 260px;
}

.logo-style {
  padding: 10px;
}

.pad-dropdown {
  padding: 20px;
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

    height: 130px;

    width: 100%;
}

.dropdown {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.dropdown-content {
  display: none;
  position: absolute;
  z-index: 100;
  width: 100%;
  cursor: pointer;
}

.drop-row {
  padding-top: 10px;
  padding-bottom: 10px;
  background-color: #E5E4E2;
}

.dropdown:hover .dropdown-content {
  background-color: #E5E4E2;
  display: block;
}

#enter-button {

  height: 36px;
  width: 50px;
  border-radius: 20px;
}

</style>