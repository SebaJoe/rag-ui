<template>
    <div class="row code-border">
        <div class="col">
            <div class="row">
                <div class="col zero-pad">
                    <prism-editor class="my-editor" @change="change_code($event)" v-model="temp_code" :highlight="highlighter"></prism-editor>
                </div>
                <div class="col-1 play-btn-col p-1 text-center">
                    <div class="row flex justify-content-center">
                        <div class="col text-center">
                            <button class="btn btn-dark" @click="execute_code">
                                <h5><i class="bi bi-play-fill"></i></h5>
                            </button>
                        </div>
                    </div>
                    <div class="row flex justify-content-center mt-4 mb-3" v-if="loading">
                        <div class="col text-center">
                            <div class="spinner-border text-light" role="status">
                            </div>
                        </div>
                    </div>
                    <div class="row flex justify-content-center mt-4 mb-3" v-if="output_error">
                        <div class="col text-center">
                            <h5><b><i class="bi bi-x-lg text-danger"></i></b></h5>
                        </div>
                    </div>
                    <div class="row flex justify-content-center mt-4 mb-3" v-else-if="code_success">
                        <div class="col text-center">
                            <h5><b><i class="bi bi-check-lg text-success"></i></b></h5>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row" v-if="has_output">
                <div class="col output-div output-class" v-html="output">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    // import Prism Editor
    import { PrismEditor } from 'vue-prism-editor';
    import 'vue-prism-editor/dist/prismeditor.min.css'; // import the styles somewhere

    // import highlighting library (you can use any library you want just return html string)
    import { highlight, languages } from 'prismjs/components/prism-core';
    import 'prismjs/components/prism-clike';
    import 'prismjs/components/prism-javascript';
    import 'prismjs/components/prism-python';
    import 'prismjs/themes/prism-tomorrow.css'; // import syntax highlighting styles

    import { KernelConnection } from "@jupyterlab/services";
    //import AnsiUp from 'ansi-up';
    import { AnsiUp } from 'ansi-up';

    export default {

        components: {
            PrismEditor,
        },
        props: {
            code: {required: true, type: String},
            kernel: Object,
            output: {required: true, type: String},
        },
        data () {
            return {
                temp_code: this.code,
                has_output: false,
                loading: false,
                output_error: false,
                code_success: false,
            }
        },
        methods: {

            highlighter(code) {
                return highlight(code, languages.python); 
            },
            change_code(event) {
                this.$emit('update:code', this.temp_code);
                this.$nextTick(() => {
                    console.log(this.code);
                });
            },
            execute_code() {
                if (!this.kernel) {
                    alert("Kernel is not available!");
                    return;
                }

                this.$emit('update:output', "");
                this.output_error = false;
                this.code_success = false;

                let connection = new KernelConnection({ model: this.kernel.model, serverSettings:this.kernel.settings, })

                console.log(KernelConnection);

                const future = connection.requestExecute({code: this.code});

                this.loading = true;
                console.log(future);

                const ansiUp = new AnsiUp();

                future.onIOPub = msg => {
                    this.loading = false;
                    if (msg.header.msg_type === 'stream') {
                        this.has_output = true;
                        //this.output = msg.content.text;
                        this.$emit('update:output', ansiUp.ansi_to_html(this.output + "\n" + msg.content.text));
                        this.code_success = true;
                    } else if (msg.header.msg_type === 'error') {
                        this.has_output = true;
                        console.log(msg.content);

                        let new_output = "";
                        for (let i = msg.content.traceback.length - 1; i >= 0; i--) {
                            new_output += msg.content.traceback[msg.content.traceback.length - 1 - i] + '\n';
                        }
                        this.$emit('update:output', ansiUp.ansi_to_html(this.output + "\n" + new_output));
                        this.output_error = true;
                    } else if (msg.header.msg_type === 'display_data') {
                        this.has_output = true;
                        let new_output = "";
                        console.log(msg.content);

                        // for (const key in msg.content.data) {
                        //     console.log(key);
                        //     if (myObject.hasOwnProperty(key)) {
                        //         console.log(key);
                        //         let value = msg.content.data[key];
                        //         if (key.includes('image')) {
                        //             console.log("What's up?");
                        //             let image_tag = `<img src="data:${key};base64,${value}" style="object-fit:contain;"/>`
                        //             this.$emit('update:output', ansiUp.ansi_to_html(this.output + "\n" + image_tag));
                        //         } else if (key.includes('text')) {

                        //         } else if (key.includes('json')) {

                        //         }
                        //     }
                        // }

                        Object.entries(msg.content.data).forEach(([key, value]) => {
                            console.log([key, value]);
                            if (key.includes('image')) {
                                console.log("What's up?");
                                let image_tag = `<img src="data:${key};base64,${value}" alt="${key}" style="object-fit:contain;">`
                                //let image_tag = '<img src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="Red dot" />';
                                this.$emit('update:output', this.output + "\n" + image_tag);
                            } else if (key.includes('text')) {

                            } else if (key.includes('json')) {

                            }
                        });
                        this.code_success = true;
                    } else if (msg.header.msg_type === 'execute_result') {
                        console.log(msg.content);
                    }
                }
            }
        },
    };
    </script>

    <style>
    /* required class */

    .output-class {
        font-family: 'Courier New', Courier, monospace;
        color: white;
        white-space: pre-wrap;
    }

    .my-editor {
        /* we dont use `language-` classes anymore so thats why we need to add background and text color manually */
        background: #2d2d2d;
        color: #ccc;

        /* you must provide font-family font-size line-height. Example: */
        font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
        font-size: 14px;
        line-height: 1.5;
        padding: 10px;
    
    }

    .code-border {
        border: 2px solid #212529;
        border-radius: 5px;
    }

    .play-btn {
        border-radius: 1px;
    }   

    .play-btn-col {
        background-color: #212529;
    }

    .zero-pad {
        padding: 0px;
    }

    /* optional class for removing the outline */
    .prism-editor__textarea:focus {
        outline: none;
    }

    .output-div {
        background-color: black;
        padding: 20px;
        max-height: 500px;
        overflow: auto;
    }

</style>