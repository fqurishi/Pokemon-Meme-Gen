import React from "react";

class Input extends React.Component {


  render() {
    return (
      <div>
        <input 
            className="ui-primary-input"  
            type = "file" 
            onChange={this.props.onChange}
        />
      </div>
    );
  }

  // componentDidUpdate() {
  //   // console.log('componentDidUpdate');
  // }

}


Input.defaultProps = {
  label: "Upload File"
}
export default Input;