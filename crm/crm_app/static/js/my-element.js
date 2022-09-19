//import {html, render} from 'https://unpkg.com/lit-html@0.7.1/lit-html.js';
import { LitElement, html, css } from "https://unpkg.com/lit-element@latest/lit-element.js?module";
import { classMap } from "https://unpkg.com/lit-html@2.2.7/directives/class-map.js"
import { styleMap } from  "https://unpkg.com/lit-html@2.2.7/directives/style-map.js"

M.AutoInit();

class MyElement extends LitElement {
  static properties = {
    classes: {},
    styles: {},
  };

  static styles = css`
  h1 { color: #fff; font-size:}
 .someclass {margin: 4px; padding: 4px; }
  .anotherclass { background-color: #26a69a; } 
  `;
  constructor() {
      super();
      this.classes = {someclass: true, anotherclass: true};
      this.styles = {color: 'lightgreen', fontFamily: 'Roboto'};
    }

  // Implement `render` to define a template for your element.

  render(){
    return html`
     <div class=${classMap(this.classes)} style=${styleMap(this.styles)}> 
        <h1>Créer un compte</h1>
     </div>
    `;
  }
}

customElements.define('my-element', MyElement);
