const { Component} = owl;

export class MobileMenu extends Component {

  toggle() {
      this.trigger("collapse-menu", { state: this.props.state });
  }
}