<template>
  <nav class="navbar sticky-top" style="background-color: white; padding: 0px">
    <div class="mx-auto" id="navtop">
      <div class="container">
        <div class="row flex justify-content-center">
          <div class="col-3 logo-style text-center">
            <img src="../assets/Cosmic-AI.jpg" height="50px">
          </div>
        </div>
      </div>
    </div>
  </nav>
  <div class="container-fluid">
    <div class="mx-auto" id="chatcol">
      <div class="container pt-4">
        <div class="row">
          <div class="col">
            <div class="row" v-for="(cell, index) in out_cells" :key="index">
              <div class="col" v-if="cell.type === 'code_response'">
                <CodeOut 
                  v-model:code="cell.text"
                  v-model:output="cell.output"
                  :kernel="kernel"
                />
              </div>
              <div class="col" v-else-if="cell.type === 'text_response'">
                <MarkOut 
                  v-model:text="cell.text"
                  :start_edit="edit_snap()"
                />
              </div>
              <div class="col" v-else>
                <MarkOut 
                  v-model:text="cell.text"
                  isUser
                />
              </div>
            </div>
            <div class="row flex justify-content-center" style="margin-top: 20px;">
              <div class="col-3 border-end rounded-start text-center hover-btn" style="padding-top: 25px; padding-bottom: 25px" @click="click_file()">
                <h5>Import .ipynb</h5>
                <input type="file" id="file_button" ref="doc" style="display: none;" @change="readfile()">
              </div>
              <div class="col-3 border-end text-center hover-btn" style="padding-top: 25px; padding-bottom: 25px" @click="add_markdown()">
                <h5>Add Markdown</h5>
              </div>
              <div class="col-3 text-center hover-btn" style="padding-top: 25px; padding-bottom: 25px" @click="add_code()">
                <h5>Add Code</h5>
              </div>
              <div class="col-3 border-start rounded-end text-center hover-btn" style="padding-top: 25px; padding-bottom: 25px" @click="export_to_notebook()">
                <h5>Export to .ipynb</h5>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <nav class="navbar fixed-bottom" :class="{'bottom-bar': !collapse_chat, 'bottom-bar-hide': collapse_chat}" style="background-color: white;">
      <div class="mx-auto" id="chatif">
        <div class="container">
          <div class="row flex justify-content-center" style="height:15px;" @mouseover="show_toggle = true;" @mouseleave="show_toggle = false;">
            <div class="chat-toggle-wrapper">
              <div class="col-3 rounded-circle chat-toggle text-center" v-if="show_toggle" @click="collapse_chat = !collapse_chat">
                <h4 style="padding-top: 10px" v-if="!collapse_chat"><i class="bi bi-chevron-down" style="color: white;"></i></h4>
                <h4 style="padding-top: 10px" v-else><i class="bi bi-chevron-up" style="color: white;"></i></h4>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col"> 
              <textarea id="chatbox" v-model="query" placeholder="Write your queries here..." @keydown.enter.prevent="send_response()"></textarea>
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
              <button type="button" id="enter-button" class="btn btn-dark" @click="send_response()">
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

  import axios from 'axios'

  import { ServerConnection, KernelAPI } from "@jupyterlab/services";

  import CodeOut from './CodeOut.vue';
  import MarkOut from './MarkOut.vue';

  import download from "downloadjs";
  import { parse } from 'vue/compiler-sfc';

  export default {
    components: {
        CodeOut,
        MarkOut,
    },
    data () {
      return {
        stream_out: "",
        query: "",
        code_out: "What's up doc",
        full_messages: {
          messages: [],
        },
        out_cells: [],
        collapse_chat: false,
        show_toggle: false,
        kernel: null,
        edit_outset: false,
        api_server_url: "http://127.0.0.1:5000/stream",
      }
    },
    async mounted () {


      function getXsrfToken() {
        const match = document.cookie.match("\\b_xsrf=([^;]*)\\b");
        return match ? match[1] : null;
      }

      const xsrfToken = getXsrfToken();

      const settings = ServerConnection.makeSettings({
        baseUrl: "http://localhost:8888/",
        headers: { "X-XSRFToken": xsrfToken },
      });

      console.log(settings.baseUrl);

      let kernel_model = await KernelAPI.startNew({}, settings);

      this.kernel = {
        model: kernel_model, 
        settings: settings,
      }

      // const future = this.kernel.requestExecute({code: "print('hello world')"});
      // future.onIOPub = msg => {
      //     if (msg.header.msg_type === 'stream') {
      //         this.has_output = true;
      //         this.output = msg.content.text;
      //     }
      // }

    },
    methods: {
      replace_code_w_cells() {
        const regex = /(?:```|~~~)(.*?)\n([\s\S]*?)\n(?:```|~~~)/g;

        const matches = [...this.out_cells[this.out_cells.length - 1].text.matchAll(regex)];

        for(let i = 0; i < matches.length; i++) {
        
          let match = matches[i];

          console.log(match);

          if (match[1] === 'python') {
            //time to cut
            let code_split = this.out_cells[this.out_cells.length - 1].text.split(match[0]);
            let ind_preserve = this.out_cells[this.out_cells.length - 1].msg_ind;
            this.out_cells[this.out_cells.length - 1].text = code_split[0];
            this.out_cells.push({
              type:"code_response",
              text: match[2],
              output: "",
              msg_ind: ind_preserve,
            })

            let leftover = (code_split.length > 1) ? code_split[1] : "";
            this.out_cells.push({
              type: "text_response",
              text: leftover,
              msg_ind: ind_preserve,
            });
          } 
        }
      },
      click_file () {
        document.getElementById("file_button").click();

      },
      edit_snap () {
        if (this.edit_outset === true) {
          return true;
        }
        return false;
      },
      add_markdown () {
        
        // let m_ind = 0;
        // if (this.out_cells.length === 0)
        //   m_ind = (this.out_cells[this.out_cells.length].type === 'query') ? this.out_cells[this.out_cells.length].msg_ind + 1: this.out_cells[this.out_cells.length].msg_ind;

        let m_ind = 0;
        if (this.out_cells.length > 0) {
          if (this.out_cells[this.out_cells.length - 1].type === 'query') {
            m_ind = this.out_cells[this.out_cells.length - 1].msg_ind + 1;
            this.full_messages.messages.push({'role': 'assistant', 'content': ""});
          } else {
            m_ind = this.out_cells[this.out_cells.length - 1].msg_ind;
          }
        } else {
          this.full_messages.messages.push({'role': 'assistant', 'content': ""});
        }

        this.edit_outset = true;
        this.out_cells.push({
          type: "text_response",
          text: "",
          msg_ind: m_ind,
        });
        this.$nextTick(function () {
          this.edit_outset = false;
        });
      },
      add_code () {
        
        let m_ind = 0;
        if (this.out_cells.length > 0) {
          if (this.out_cells[this.out_cells.length - 1].type === 'query') {
            m_ind = this.out_cells[this.out_cells.length - 1].msg_ind + 1;
            this.full_messages.messages.push({'role': 'assistant', 'content': ""});
          } else {
            m_ind = this.out_cells[this.out_cells.length - 1].msg_ind;
          }
        } else {
          this.full_messages.messages.push({'role': 'assistant', 'content': ""});
        }

        this.out_cells.push({
          type: "code_response",
          text: "",
          msg_ind: m_ind,
          output: "",
        });
      },
      readfile () {
        let file = this.$refs.doc.files[0];
        const reader = new FileReader();
        if(file.name.includes('.ipynb')) {
          reader.onload = (res) => {
            let parsed_file = JSON.parse(res.target.result);
            let m_ind = this.full_messages.messages.length;
            for (let i = 0; i < parsed_file.cells.length; i++) {

              let source_text = (typeof parsed_file.cells[i].source === 'string') ? parsed_file.cells[i].source : parsed_file.cells[i].source.join('\n');

              if (parsed_file.cells[i].cell_type === 'code') {
                this.out_cells.push({
                  type: "code_response",
                  text: source_text,
                  msg_ind: m_ind,
                  output: "",
                });

              } else {
                this.out_cells.push({
                  type: "text_response",
                  text: source_text,
                  msg_ind: m_ind,
                });
              }

            }
            this.full_messages.messages.push({'role': 'assistant', 'content': ""});
            this.correct_messages();
          }
          reader.onerror = (err) => console.log(err);
          reader.readAsText(file);
        }
      },
      correct_messages() {
        for (let i = 0; i < this.full_messages.messages.length; i++) {
          this.full_messages.messages[i].content = "";
        }
        for (let i = 0; i < this.out_cells.length; i++) {
          if (this.out_cells[i].type === 'text_response' || this.out_cells[i].type === 'query')
            this.full_messages.messages[this.out_cells[i].msg_ind].content += this.out_cells[i].text;
          if (this.out_cells[i].type === 'code_response')
            this.full_messages.messages[this.out_cells[i].msg_ind].content += `\`\`\`python\n${this.out_cells[i].text}\n\`\`\``;
        }
      },
      export_to_notebook() {
        const notebook = {
          "metadata": {
            "kernelspec": {
              "display_name": "Python 3",
              "language": "python",
              "name": "python3"
            },
            "language_info": {
              "codemirror_mode": {
                "name": "ipython",
                "version": 3
              },
              "file_extension": ".py",
              "mimetype": "text/x-python",
              "name": "python",
              "nbconvert_exporter": "python",
              "pygments_lexer": "ipython3",
              "version": "3.x"
            }
          },
          "nbformat": 4,
          "nbformat_minor": 4,
          "cells": this.out_cells.map(cell => { 
            if (cell.type === 'text_response') {
              return {
                "cell_type": "markdown",
                "metadata": {},
                "source": cell.text,
                "outputs": []
              }
            } else if (cell.type === 'code_response') {
              return {
                "cell_type": "code",
                "metadata": {},
                "source": cell.text,
                "outputs": (cell.output) ? [{ "output_type": "stream", "name": "stdout", "text": cell.output}]: [],
              }
            } else {
              return {
                "cell_type": "markdown",
                "metadata": {},
                "source": `<span style="background-color:#a9cce3;">${cell.text}</span>`,
                "outputs": []
              }
            }
          })
        };

        //downloading time
        const current_date = new Date();
        let end_object = JSON.stringify(notebook);
        end_object = end_object.replace(/[\u007F-\uFFFF]/g, function(chr) {
                return "\\u" + ("0000" + chr.charCodeAt(0).toString(16)).substr(-4);
        });
        download(end_object, "export_cosmicAI_nb_" + current_date.toString().replace(" ", "_") + ".ipynb", 'application/json');
      },
      send_response() {
        let prompt = this.query;

        this.query = "";

        this.correct_messages();

        this.full_messages.messages.push({'role': 'user', 'content': prompt});

        this.out_cells.push({
          type: "query",
          text: prompt,
          msg_ind: this.full_messages.messages.length,
        });

        this.out_cells.push({
          type: "text_response",
          text: "",
          msg_ind: this.full_messages.messages.length,
        });

        axios.post(this.api_server_url, this.full_messages)
          .then(response => {

            this.full_messages.messages.push({'role': 'assistant', 'content': ""});

            console.log(response);

            console.log("What's crackign");

            const eventSource = new EventSource(this.api_server_url);

            eventSource.onerror = (e) => console.log("Error:", e);


            eventSource.onmessage = (e) => {
              if (e.data !== "[DONE]") {
                console.log(JSON.stringify(e.data));
                let stext = e.data.replaceAll("<NEWLINE>", '\n');
                // if (!stext.endsWith(" ")) {
                //   stext += " ";
                // }
                this.out_cells[this.out_cells.length - 1].text += stext;
                this.full_messages.messages[this.full_messages.messages.length - 1].content += stext;
                this.replace_code_w_cells();
              } else {
                console.log("Connection closed")
                eventSource.close()
              }
            };

          }) 
          .catch(error => {
            console.error("There was an error!", error);
            
          });
      },
    }
  }

</script>


<style>

code[class*="language-"] {
  color: black;
}

.chat-toggle {
  background-color: black;
  position: absolute;
  height: 50px;
  width: 50px;
}

.chat-toggle-wrapper {
  height: 150px;
  width: 150px;
  padding: 50px;
  position: absolute;
  margin-top: -75px;
}

.bottom-bar {
  height: 220px;
  transition: height 0.3s ease;
}

.bottom-bar-hide {
  height:15px;
  transition: height 0.3s ease;
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

.hover-btn:hover {
  cursor: pointer;
  background-color: #F9f9f9;
}

#chatbox {
    border: none;
    overflow: auto;
    outline: none;


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