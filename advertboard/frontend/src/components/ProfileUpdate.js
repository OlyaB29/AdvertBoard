import React, {useEffect, useRef, useState} from 'react';
import {useForm} from "react-hook-form";
import {useLocation, useNavigate, useParams} from "react-router-dom";
import AdvertBoardService from './AdvertBoardService';
import {BsXOctagon} from "react-icons/bs";

const advertBoardService = new AdvertBoardService();


function ProfileUpdate() {

    const [profile, setProfile] = useState({user: {username: null, email: null}});
    const {id} = useParams();
    const navigate = useNavigate();
    const location = useLocation();
    const [access, setAccess] = useState(localStorage.getItem('accessToken'));
    const {register, formState: {errors, isValid}, handleSubmit, setValue} = useForm({mode: "onBlur"});
    const [avatar, setAvatar] = useState();
    const [isUpdate, setIsUpdate] = useState(false);
    const [data, setData] = useState({});

    useEffect(() => {
        if (!isUpdate) {
            advertBoardService.getProfile(id, access).then(function (result) {
                console.log(result);
                if (result) {
                    if (result.access) {
                        localStorage.setItem('accessToken', result.access);
                        setAccess(result.access);
                        localStorage.setItem('refreshToken', result.refresh);
                    } else {
                        setProfile(result);
                        setValue('name', result.name);
                        setValue('phone', result.phone);
                    }
                } else {
                    navigate('/login', {replace: true, state: {from: location}});
                }
            })
        }
    }, [id, access]);

    const selAvatar = useRef();
    const img = useRef();

    const selectAvatar = () => {
        selAvatar.current.click();
    }

    const addAvatar = (event) => {
        const avatar = event.target.files[0];
        const reader = new FileReader();
        reader.onload = function () {
            img.current.src = reader.result;
        };
        reader.readAsDataURL(avatar);
        setAvatar(avatar);
    }

    const deleteAvatar = (event) => {
        img.current.src = "/img/No_photo.png";
        setAvatar();
    }

    useEffect(() => {
        if (isUpdate) {
            advertBoardService.updateProfile(id, data, access).then(function (r) {
                if (r) {
                    if (r.access) {
                        console.log(r)
                        localStorage.setItem('accessToken', r.access);
                        setAccess(r.access);
                        localStorage.setItem('refreshToken', r.refresh);
                    } else {
                        alert('?????????????? ????????????????')
                    }
                } else {
                    navigate('/login', {replace: true, state: {from: location}});
                }
            });
        }
    }, [isUpdate, access, data])


    const onSubmit = (data) => {
        alert(JSON.stringify(data));
        const formData = new FormData();
        formData.append('name', data.name);
        formData.append('phone', data.phone);
        console.log(avatar)
        if (avatar) {
            console.log('avatar');
            formData.append('avatar', avatar);
        }

        setIsUpdate(true);
        setData(formData);
    }

    return (
        <div className='profile-update'>
            <div className="container" style={{width: 900}}>
                <h2>???????????????????????????? ?????????????? {profile.user.username} </h2>
                <form onSubmit={handleSubmit(onSubmit)}>
                    <div className="row">
                        <div className="form-group col-md-5">
                            <div className="add-avatar" onClick={selectAvatar}>
                                <img src={profile.avatar ? profile.avatar : "/img/No_photo.png"} ref={img} alt=""/>
                                <BsXOctagon className="delete-avatar" onClick={(event) => {
                                    event.stopPropagation();
                                    deleteAvatar()
                                }}/>
                            </div>
                            <input className="hidden" type="file" ref={selAvatar} onChange={addAvatar}
                                   accept="image/*,.png,.jpg,.gif"/>
                        </div>
                        <div className="form-group col-md-7">
                            <label>
                                ??????:
                                <input className="form-control"
                                       {...register("name", {
                                           required: "???????? ?????????????????????? ?? ????????????????????",
                                           maxLength: {value: 50, message: "???????????????? 50 ????????????????"},
                                           pattern: {
                                               value: /^[a-z??-????\s]+$/iu,
                                               message: "???????? ?????????? ?????????????????? ???????????? ?????????????? ?????? ?????????????????? ??????????"
                                           }
                                       })}
                                />
                                {errors?.name &&
                                    <div className="error">
                                        <p style={{marginBottom: 0}}>{errors.name.message}</p>
                                    </div>}
                            </label>
                            <label>
                                ??????????????:
                                <input className="form-control"
                                       {...register("phone", {
                                           required: "???????? ?????????????????????? ?? ????????????????????",
                                           pattern: {
                                               value: /(?:\+375|80)\s?\(?\d\d\)?\s?\d\d(?:\d[\-\s]\d\d[\-\s]\d\d|[\-\s]\d\d[\-\s]\d\d\d|\d{5})/,
                                               message: "???????????????????????? ????????????????"
                                           }
                                       })}
                                />
                                {errors?.phone &&
                                    <div className="error">
                                        <p style={{marginBottom: 0}}>{errors.phone.message}</p>
                                    </div>}
                            </label>
                            <button className="btn" type='submit' disabled={!isValid}>?????????????????? ??????????????????</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>

    );
}

export default ProfileUpdate;
