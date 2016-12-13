global mesh_precision;
global horizontal;
global vertical;
global goal;

mesh_precision = 40;
horizontal = 200;
vertical = 100;
goal = [99,40];

function mesh_coordinates = mesh_coordinates(position)
  global vertical;
  global horizontal;
  global mesh_precision;
  mesh_coordinates = [round(position(1)*mesh_precision/min(horizontal,vertical))+1,round(position(2)*mesh_precision/min(horizontal,vertical))+1];
endfunction

function neighbours = get_neighbours(mesh_coordinate)
  global horizontal;
  global vertical;
  neighbours = [];
  if mesh_coordinate(1)-1>0
    neighbours = [neighbours;[mesh_coordinate(1)-1,mesh_coordinate(2)]];
  endif
  if mesh_coordinate(1)+1<=mesh_coordinates([horizontal,vertical])(1)
    neighbours = [neighbours;[mesh_coordinate(1)+1,mesh_coordinate(2)]];
  endif
  if mesh_coordinate(2)-1>0
    neighbours = [neighbours;[mesh_coordinate(1),mesh_coordinate(2)-1]];
  endif
  if mesh_coordinate(2)+1<=mesh_coordinates([horizontal,vertical])(2)
    neighbours = [neighbours;[mesh_coordinate(1),mesh_coordinate(2)+1]];
  endif
endfunction

function heuristic = get_heuristic(mesh_coordinate)
  global goal;
  heuristic = sqrt((mesh_coordinate(1)-mesh_coordinates(goal)(1))^2+(mesh_coordinate(2)-mesh_coordinates(goal)(2))^2);
endfunction

function path = astar(position)
  global goal;
  goal_mesh = mesh_coordinates(goal);
  mesh_coordinate = mesh_coordinates(position);
  queue = [mesh_coordinate,get_heuristic(mesh_coordinate),0];
  explored = [];
  parent = [];
  while !size(queue)==0
    mesh_coordinate = queue(1,1:2);
    cost = queue(1,4);
    explored = [explored;mesh_coordinate];
    if mesh_coordinate==goal_mesh
      node = goal_mesh;
      figure();
      
      while (true)
        [~,index4] = ismember(node,parent(:,1:2),'rows');
        if !index4
          axis([0 10 0 10]);
          return
        endif
        node = parent(index4,3:4);
        rectangle_position = [node-0.5,1,1];
        rectangle("position",rectangle_position,"curvature",1,"FaceColor",'r');
        axis("square");
      endwhile
    endif
    queue = queue(2:end,:);
    neighbours = get_neighbours(mesh_coordinate);
    old_index = ismember(mesh_coordinate,queue(:,1:2));
    for i=1:size(neighbours)
      
      [~,index1] = ismember(neighbours(i,:),queue(:,1:2),'rows');
      [~,index2] = ismember(neighbours(i,:),explored,'rows');
      if !index1 && !index2
        queue = [queue;[neighbours(i,:),cost+1+get_heuristic(neighbours(i,:)),cost+1]];
        parent = [parent;[neighbours(i,:),mesh_coordinate]];
      elseif index1 && queue(index1,:)(4)>cost+1
        queue(index1,:) = [neighbours(i,:),cost+1+get_heuristic(neighbours(i,:)),cost+1];
        [~,index3] = ismember(neighbours(i,:),parent(:,1:2));
        queue(index3,:) = [neighbours(i,:),mesh_coordinate];
      endif
    endfor
    [s,i] = sort(queue(:,3));
    queue=queue(i,:);
  endwhile
  return
endfunction

astar([10,10])
axis("square")