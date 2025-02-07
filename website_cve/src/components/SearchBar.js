import React, { Component } from 'react'
import DisplayResult from './DisplayResult';
import Spinner from './Spinner';

export default class SearchBar extends Component {
    constructor(){
        super();
        this.state = {
            url: '',
            scrapedDataObj: '',
            loading: false
        }
    }

    sanitizeUrl(url) {
        try {
            const parsedUrl = new URL(url); // Parse the URL
            const domain = parsedUrl.hostname // Get hostname or pathname
            return domain.replace(/^www\./, ''); // Remove "www." if it exists
        } catch (e) {
            console.log("here")
            return url.replace(/\//g, '');
        }
    }

    handleOnClick = async ()=>{
        this.setState({scrapedDataObj: ''})
        if (this.state.url !== ''){

            let sanitizedUrl = this.sanitizeUrl(this.state.url)

            
            console.log("non empty field")
            console.log(sanitizedUrl)
            this.setState({loading: true})

            let data = await fetch(`http://127.0.0.1:8000/${sanitizedUrl}`)
            let parsedData = await data.json()
            console.log(parsedData)
            this.setState({scrapedDataObj: parsedData})
            console.log(this.state.scrapedDataObj)

            this.setState({loading: false})
        }
        else{
            console.log("empty field")
        }
    }

    handleOnChange =(event) =>{
        this.setState({url: event.target.value})
    }
    render() {
        let {searchPlaceholder, buttonText} = this.props
        return (
            <div className="container border mt-5">
                <h1 className="mx-auto">Wuln Wide Web</h1>
                <input className="form-control mr-sm-2 my-4" type="search"  onChange={this.handleOnChange} placeholder={searchPlaceholder} value={this.state.url} style={{width:400}}aria-label="Search"/>
                <button className="btn btn-primary my-2" onClick={this.handleOnClick} >{buttonText}</button>
                {this.state.loading ? <Spinner/> : null}
                {this.state.scrapedDataObj?<DisplayResult scrapedDepObj={this.state.scrapedDataObj}/>:''}
            </div>
    )
  }
}


