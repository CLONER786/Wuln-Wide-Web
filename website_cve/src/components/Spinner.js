import React from 'react'
import spinner from './Spinner-2.gif'

export default function Spinner(){
    return(
        <div class="container m-3">
            <img src={spinner} alt="Loading" />
        </div>
    )
}