from django.shortcuts import render, redirect
from .models import *
from django.views.decorators.cache import cache_control
import re
import json

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            return redirect('logout')
        else:
            return render(request, 'index.html')
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        pattern = r"^\S+@\S+\.\S+$"
        if re.match(pattern, email):
            try:
                user_object = UserDetails.objects.get(email=email)
            except UserDetails.DoesNotExist:
                user_object = None
            if user_object:
                unew = UserDetails.objects.get(email=email)
                checked = unew.pass_word
                if checked == password:
                    RTO = 'RTO'
                    if UserDetails.objects.filter(email=unew.email, pass_word=checked, account_type=RTO).exists():
                        user_id = UserDetails.objects.get(
                            email=request.POST['email'], pass_word=request.POST['password'])
                        request.session['user_id'] = user_id.id
                        return redirect('RTO')

                    user = 'user'
                    if UserDetails.objects.filter(email=email, pass_word=password, account_type=user).exists():
                        user_id = UserDetails.objects.get(
                            email=request.POST['email'], pass_word=request.POST['password'])
                        request.session['user_id'] = user_id.id
                        return redirect('user')

                    agent = 'agent'
                    if UserDetails.objects.filter(email=email, pass_word=password, account_type=agent).exists():
                        user_id = UserDetails.objects.get(
                            email=request.POST['email'], pass_word=request.POST['password'])
                        request.session['user_id'] = user_id.id
                        return redirect('agent')
                    else:
                        return redirect('index')
                else:
                    email = request.POST['email']
                    passerr = "password Incorrect!"
                    return render(request, 'index.html', {'passerr': passerr, 'email': email})
            else:
                noemailerr = request.POST['email']
                return render(request, 'index.html', {'noemailerr': noemailerr})
        else:
            email = request.POST['email']
            emailerr = 'invalid email'
            return render(request, 'index.html', {'emailerr': emailerr, 'email': email})
    else:
        return redirect('index')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def RTO(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
        else:
            return redirect('index')
        RTO = UserDetails.objects.filter(id=user_id)
        users = UserDetails.objects.all()
        vehicle_list = AgentVehicle.objects.all()
        return render(request, 'RTO.html', {'RTO': RTO, 'vehicle_list': vehicle_list, 'users': users})
    else:
        return redirect('/')

def RTOVehicleRegNoAddForm(request, id):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
            if request.method == "POST":
                reg_num = request.POST['reg_num']
                if AgentVehicle.objects.filter(vehicle_registration=reg_num).exists():
                    reg_num = request.POST['reg_num']
                    RTO = UserDetails.objects.filter(id=user_id)
                    users = UserDetails.objects.all()
                    vehicle_list = AgentVehicle.objects.all()
                    return render(request, 'RTO.html', {'RTO': RTO, 'vehicle_list': vehicle_list, 'users': users,'reg_num':reg_num})
                else:
                    RTO = UserDetails.objects.filter(id=user_id)
                    users = UserDetails.objects.all()
                    reg_num = request.POST['reg_num']
                    get_vehicle = AgentVehicle.objects.get(id=id)
                    get_vehicle.vehicle_registration = reg_num
                    get_vehicle.save()
                    return redirect('RTO')
            else:
                return redirect('RTO')
        else:
            return redirect('index')
    else:
        return redirect('/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
            user = UserDetails.objects.filter(id=user_id)
            vehicle_list = AgentVehicle.objects.filter(user_id=user_id)
            users = UserDetails.objects.all()
            return render(request, 'user.html', {'user': user,'users':users,'vehicle_list':vehicle_list})
        else:
            return redirect('index')
    else:
        return redirect('index')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def agent(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
            agent = UserDetails.objects.filter(id=user_id)
            vehicle_list = AgentVehicle.objects.filter(agent_id=user_id)
            return render(request, 'agent.html', {'agent': agent, 'vehicle_list': vehicle_list})
        else:
            return redirect('index')
    else:
        return redirect('index')

def listPageAgent(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
            agent = UserDetails.objects.filter(id=user_id)
            vehicle_list = AgentVehicle.objects.filter(agent_id=user_id)
            vehicle_ind = AgentVehicle.objects.get(user_id=17)
            dicts = json.loads(vehicle_ind.name)
            print('dicts : ',dicts)
            print("dicts['Name']: ", dicts["Name"])
            return render(request, 'listPageAgent.html', {'agent': agent, 'vehicle_list': vehicle_list})
        else:
            return redirect('index')
    else:
        return redirect('index')

def agentVehicleAddForm(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
            vin_number = request.POST['vin_number']
            vehicleYear = request.POST['vehicleYear']
            vehicleMake = request.POST['vehicleMake']
            vehicleModel = request.POST['vehicleModel']
            color = request.POST['color']
            mileage = request.POST['mileage']
            nesw = request.POST['nesw']
            vehiclename = request.POST['vehiclename']
            name = request.POST['name']
            address = request.POST['address']
            districtSelect = request.POST['districtSelect']
            citySelect = request.POST['citySelect']
            zip = request.POST['zip']
            email = request.POST['email']
            if request.method == "POST":
                if AgentVehicle.objects.filter(vin_number=vin_number).exists():
                    user_id = request.session['user_id']
                    agent = UserDetails.objects.filter(id=user_id)
                    vehicle_list = AgentVehicle.objects.filter(
                        agent_id=user_id)
                    registered = 'this vehicle is registered'
                    return render(request, 'agent.html', {'registered': registered,
                                                          'vehicleYear': vehicleYear, 'vehicleMake': vehicleMake,
                                                          'vehicleModel': vehicleModel, 'color': color, 'mileage': mileage, 'vin_number': vin_number,
                                                          'nesw': nesw, 'vehiclename': vehiclename, 'name': name, 'address': address, 'districtSelect': districtSelect,
                                                          'citySelect': citySelect, 'zip': zip, 'email': email, 'vehicle_list': vehicle_list})
                else:
                    email_without_dot = email.replace('.', '')
                    pass_strip = email_without_dot.split("@")[0]
                    pass_word = pass_strip + str(123)
                    user_create = UserDetails(
                        username=name, email=email, pass_word=pass_word, account_type="User")
                    user_create.save()
                    user_create_id = user_create.id
                    agent_details = json.dumps({"Name" : name,"Email" : email,"Address":address,"District":districtSelect,"City":citySelect,"Zip":zip,"user_id":user_id})
                    agent = UserDetails.objects.filter(id=user_id)
                    vehicle_list = AgentVehicle.objects.filter(
                        agent_id=user_id)
                    add_vehicle = AgentVehicle(vehicle_registration='', vin_number=vin_number, vehicle_year=vehicleYear, vehicle_make=vehicleMake, vehicle_model=vehicleModel, color=color,
                                               mileage=mileage, number_etched_into_windows=nesw, vehicle_name=vehiclename, name=agent_details, address=address, state=districtSelect, city=citySelect, zip_code=zip, email=email, agent_id=user_id, user_id=user_create_id)
                    add_vehicle.save()
                    return render(request, 'agent.html', {'agent': agent, 'vehicle_list': vehicle_list})

            else:
                return redirect('agent')
        else:
            return redirect('index')
    else:
        return redirect('index')

def agentVehicleEditForm(request, id):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
            if request.method == "POST":
                user_id = request.session['user_id']
                agent = UserDetails.objects.filter(id=user_id)
                vehicle_list_edit = AgentVehicle.objects.filter(id=id)
                vehicle_list = AgentVehicle.objects.filter(agent_id=user_id)
                return render(request, 'agent.html', {'agent': agent, 'vehicle_list_edit': vehicle_list_edit, 'vehicle_list': vehicle_list})
            else:
                return redirect('agent')
        else:
            return redirect('index')
    else:
        return redirect('index')

def agentVehicleEditFormSubmit(request, id):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
            vin_number = request.POST['vin_number']
            vehicleYear = request.POST['vehicleYear']
            vehicleMake = request.POST['vehicleMake']
            vehicleModel = request.POST['vehicleModel']
            color = request.POST['color']
            mileage = request.POST['mileage']
            nesw = request.POST['nesw']
            vehiclename = request.POST['vehiclename']
            name = request.POST['name']
            address = request.POST['address']
            districtSelect = request.POST['districtSelect']
            citySelect = request.POST['citySelect']
            zip = request.POST['zip']
            email = request.POST['email']
            if AgentVehicle.objects.exclude(id=id).filter(vin_number=vin_number).exists():
                vehicle_list = AgentVehicle.objects.filter(agent_id=user_id)
                veh_id = id
                registered_id = 'this vehicle is registered'
                return render(request, 'agent.html', {'registered_id': registered_id,
                                                      'vehicleYear': vehicleYear, 'vehicleMake': vehicleMake,
                                                      'vehicleModel': vehicleModel, 'color': color, 'mileage': mileage, 'vin_number': vin_number,
                                                      'nesw': nesw, 'vehiclename': vehiclename, 'name': name, 'address': address, 'districtSelect': districtSelect,
                                                      'citySelect': citySelect, 'zip': zip, 'email': email, 'vehicle_list': vehicle_list, 'veh_id': veh_id})
            else:
                vehicle_list = AgentVehicle.objects.filter(agent_id=user_id)
                add_vehicle = AgentVehicle.objects.get(id=id)
                add_vehicle.vehicle_registration = add_vehicle.vehicle_registration
                add_vehicle.vin_number = vin_number
                add_vehicle.vehicle_year = vehicleYear
                add_vehicle.vehicle_make = vehicleMake
                add_vehicle.vehicle_model = vehicleModel
                add_vehicle.color = color
                add_vehicle.mileage = mileage
                add_vehicle.number_etched_into_windows = nesw
                add_vehicle.vehicle_name = vehiclename
                add_vehicle.name = name
                add_vehicle.address = address
                add_vehicle.state = districtSelect
                add_vehicle.city = citySelect
                add_vehicle.zip_code = zip
                add_vehicle.email = email
                add_vehicle.user_id = add_vehicle.user_id
                add_vehicle.agent_id = add_vehicle.agent_id
                add_vehicle.save()
                return redirect('agent')
        else:
            return redirect('index')
    else:
        return redirect('index')


def logout(request):
    if 'user_id' in request.session:
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')
